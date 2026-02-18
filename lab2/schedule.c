/*
 * Lab 2: NFDH and FFDH for 2D Strip Packing (scheduling parallel tasks).
 * Input: task file (lines "r_j t_j"), n = number of EMs, algorithm (NFDH|FFDH).
 * Output: T(S), T', epsilon, runtime (s). Tasks ordered by counting sort (by t_j decreasing).
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>

typedef struct { int r, t; } task_t;

static int n_em;           /* strip width = number of EMs */
static task_t *tasks;     /* sorted by t decreasing */
static int m;

/* Lower bound: T' = (1/n) * sum_j (r_j * t_j) */
static double lower_bound(void)
{
    long long sum = 0;
    for (int j = 0; j < m; j++)
        sum += (long long)tasks[j].r * tasks[j].t;
    return (double)sum / n_em;
}

/* Counting sort by t (height) descending. t in [1, 100]. */
static void sort_by_height_decreasing(void)
{
    int count[101];
    memset(count, 0, sizeof count);
    for (int j = 0; j < m; j++)
        count[tasks[j].t]++;
    /* Prefix: count[t] = number of tasks with height >= t (for descending) */
    for (int t = 99; t >= 0; t--)
        count[t] += count[t + 1];
    task_t *out = malloc((size_t)m * sizeof(task_t));
    for (int j = m - 1; j >= 0; j--) {
        int t = tasks[j].t;
        int pos = --count[t];
        out[pos] = tasks[j];
    }
    memcpy(tasks, out, (size_t)m * sizeof(task_t));
    free(out);
}

/* NFDH: Next Fit Decreasing Height. One level at a time. */
static double nfdh(void)
{
    double current_y = 0;
    int used_width = 0;
    int level_height = 0;

    for (int j = 0; j < m; j++) {
        int r = tasks[j].r, t = tasks[j].t;
        if (used_width + r > n_em) {
            current_y += level_height;
            used_width = 0;
            level_height = 0;
        }
        used_width += r;
        if (t > level_height)
            level_height = t;
    }
    return current_y + level_height;
}

/* Tournament tree (max winner): leaves = levels, value = free width (n - used).
   Find first leaf with free >= r in O(log L). */
#define MAX_LEVELS 10000
static int level_used[MAX_LEVELS];
static int level_height[MAX_LEVELS];
static double level_y[MAX_LEVELS];
static int n_levels;

static int tree_size;      /* number of leaves in tree (power of 2) */
static int *tree;          /* max tree: tree[i] = max of leaves in segment */

static int tree_first_fit(int need)
{
    if (tree[1] < need)  /* root = max over leaves; -1 = unused */
        return -1;
    int i = 1;
    while (i < tree_size) {
        int left = i * 2;
        if (tree[left] >= need)
            i = left;
        else
            i = left + 1;
    }
    return i - tree_size;  /* leaf index 0..n_levels-1 */
}

static void tree_update(int leaf_idx, int free_val)
{
    int i = tree_size + leaf_idx;
    tree[i] = free_val;
    for (i /= 2; i >= 1; i /= 2) {
        int l = tree[2*i], r = tree[2*i+1];
        tree[i] = (l >= r) ? l : r;
    }
}

static void tree_add_level(double y, int used, int h)
{
    level_y[n_levels] = y;
    level_used[n_levels] = used;
    level_height[n_levels] = h;
    int free = n_em - used;
    int leaf = tree_size + n_levels;
    tree[leaf] = free;
    for (int i = leaf / 2; i >= 1; i /= 2)
        tree[i] = (tree[2*i] >= tree[2*i+1]) ? tree[2*i] : tree[2*i+1];
    n_levels++;
}

/* FFDH: First Fit Decreasing Height. Tournament tree over levels. */
static double ffdh(void)
{
    n_levels = 0;
    int cap = 1;
    while (cap < MAX_LEVELS)
        cap *= 2;
    tree_size = cap;
    tree = malloc((size_t)(2 * tree_size) * sizeof(int));
    for (int i = 0; i < 2 * tree_size; i++)
        tree[i] = -1;  /* unused leaves never chosen (need >= 1) */

    double total_height = 0;

    for (int j = 0; j < m; j++) {
        int r = tasks[j].r, t = tasks[j].t;
        int idx = tree_first_fit(r);
        if (idx < 0) {
            /* New level */
            double y = total_height;
            if (n_levels > 0) {
                double max_end = 0;
                for (int k = 0; k < n_levels; k++) {
                    double end = level_y[k] + level_height[k];
                    if (end > max_end)
                        max_end = end;
                }
                y = max_end;
            }
            total_height = y + t;
            tree_add_level(y, r, t);
        } else {
            level_used[idx] += r;
            if (t > level_height[idx])
                level_height[idx] = t;
            tree_update(idx, n_em - level_used[idx]);
        }
    }

    double makespan = 0;
    for (int k = 0; k < n_levels; k++) {
        double end = level_y[k] + level_height[k];
        if (end > makespan)
            makespan = end;
    }
    free(tree);
    return makespan;
}

static double wall_time(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main(int argc, char **argv)
{
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <tasks_file> <n_EM> <NFDH|FFDH>\n", argv[0]);
        return 1;
    }
    n_em = atoi(argv[2]);
    if (n_em <= 0) {
        fprintf(stderr, "Error: n_EM must be positive\n");
        return 1;
    }
    int use_ffdh = 0;
    if (strcmp(argv[3], "FFDH") == 0)
        use_ffdh = 1;
    else if (strcmp(argv[3], "NFDH") != 0) {
        fprintf(stderr, "Error: algorithm must be NFDH or FFDH\n");
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (!f) {
        perror(argv[1]);
        return 1;
    }
    m = 0;
    int cap = 1024;
    tasks = malloc((size_t)cap * sizeof(task_t));
    while (fscanf(f, "%d %d", &tasks[m].r, &tasks[m].t) == 2) {
        if (tasks[m].r <= 0 || tasks[m].t <= 0 || tasks[m].r > n_em) {
            fprintf(stderr, "Error: invalid task r=%d t=%d\n", tasks[m].r, tasks[m].t);
            fclose(f);
            free(tasks);
            return 1;
        }
        m++;
        if (m >= cap) {
            cap *= 2;
            tasks = realloc(tasks, (size_t)cap * sizeof(task_t));
        }
    }
    fclose(f);
    if (m == 0) {
        fprintf(stderr, "Error: no tasks read\n");
        free(tasks);
        return 1;
    }

    sort_by_height_decreasing();

    double T_prime = lower_bound();
    if (T_prime < 1e-9)
        T_prime = 1e-9;

    double t0 = wall_time();
    double T_s = use_ffdh ? ffdh() : nfdh();
    double elapsed = wall_time() - t0;

    double epsilon = (T_s - T_prime) / T_prime;

    printf("T(S)=%.6f\n", T_s);
    printf("T'=%.6f\n", T_prime);
    printf("epsilon=%.6f\n", epsilon);
    printf("time=%.6f\n", elapsed);

    free(tasks);
    return 0;
}
