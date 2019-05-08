#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <cstdlib>
#include <time.h>
#include <fstream>

#include <omp.h>

 
using namespace std;
 
// Utils
const string USAGE_INFO = "Params: numberOfData, numberOfProcessors, numberOfBucketsPerProcessor.\nUsage: ./alg1 1000 4 16\n";
 
double times[8];
int time_i = 0;

double calculateTimeElapsed(timespec start, timespec finish) {
    return (finish.tv_sec - start.tv_sec) + ((finish.tv_nsec - start.tv_nsec) / 1000000000.0);
}
 
bool isNumber(string s) {
    return !s.empty() && all_of(s.begin(), s.end(), ::isdigit);
}
 
bool checkIfSorted(float* data, int n) {
    for (int i = 0; i < n - 1; i++) {
        if (data[i] > data[i+1]) {
            return false;
        }
    }
    return true;
}

void measureTime(std::string label, double startTime) {
    double measuredTime = (omp_get_wtime() - startTime);
    times[time_i] = measuredTime;
    time_i += 1;
}
 
// Function to generate data
float* generateData(int n) {
    float* data = new float[n];
    int i;
 
    #pragma omp parallel
    {
        unsigned int seed = omp_get_thread_num();
        #pragma omp for private (i)
        for (i = 0; i < n; i++) {
            data[i] = ((double) rand_r(&seed)) / RAND_MAX;
        }
    }
 
    return data;
}
 
float* bucketSort(float* data, int proc, int nPerProc, int buckPerProc)
{
    double startTime;
 
    startTime = omp_get_wtime();
 
    int n = proc * nPerProc;
    int numberOfBuckets = proc * buckPerProc;
    int* bucketsIndexes = new int[numberOfBuckets];
    float** buckets = new float*[numberOfBuckets];
 
    for (int i = 0; i < numberOfBuckets; i++) {
        buckets[i] = new float[n];
        bucketsIndexes[i] = 0;
    }

    measureTime("Sorting initialization", startTime); // no4
 
 
    startTime = omp_get_wtime();
 
    #pragma omp parallel
    {
        unsigned int seed = omp_get_thread_num();
        for (int i = 0; i < n; i++)
        {
            
            float data = ((double) rand_r(&seed)) / RAND_MAX;
            int bi = numberOfBuckets * data; // Index in bucket
            if (bi == numberOfBuckets) {
                bi--; 
            } // Hack to handle 1
            #pragma omp critical 
            {
                buckets[bi][bucketsIndexes[bi]] = data;
                bucketsIndexes[bi]++;
            }
        }
    }
    
 
    measureTime("Splitting between buckets", startTime); // no5

    startTime = omp_get_wtime();
 
    #pragma omp parallel
    {
        int i;
        int bucketStart = buckPerProc * omp_get_thread_num();
        int bucketStop = bucketStart + buckPerProc - 1;
 
        for (i = bucketStart; i <= bucketStop; i++) {
            sort(buckets[i], buckets[i] + bucketsIndexes[i]);
        }
    }
 
 
    measureTime("Sorting individual buckets", startTime); // no6
 
    startTime = omp_get_wtime();
 
    int* divideIndexes = new int[proc + 1];
    int sum = 0;
    divideIndexes[0] = 0;
    for (int i = 0; i < numberOfBuckets; i++) {
        int x = (int)(i / buckPerProc);
        if (i % buckPerProc == 0) {
            divideIndexes[x + 1] = divideIndexes[x];
        }
 
        divideIndexes[x + 1] += bucketsIndexes[i];
        sum += bucketsIndexes[i];
    }

    int index;
    float* res = new float[n];
    #pragma omp parallel shared(res) private(index)
    {
        int bucketStart = buckPerProc * omp_get_thread_num();
        int bucketStop = bucketStart + buckPerProc - 1;

        index = divideIndexes[omp_get_thread_num()];
        for (int i = bucketStart; i <= bucketStop; i++) {
            for (int j = 0; j < bucketsIndexes[i]; j++) {
                res[index++] = buckets[i][j];
            }
        }
    }
 
    measureTime("Merging buckets", startTime); // no7
 
    return res;
}
 
 
 
int main(int argc,  char** argv)
{
    if (argc != 4 || !isNumber(argv[1]) || !isNumber(argv[2]) || !isNumber(argv[3])) {
        cerr << USAGE_INFO;
        return 1;
    }

    for (int i=0; i < 8; i++) {
        times[i] = 0;
    }
 
    const int n = atoi(argv[1]); 
    const int proc = atoi(argv[2]); // no 1
    const int buckPerProc = atoi(argv[3]); // no 2
    const int nPerProc = (int) (n / proc);
    
    times[0] = proc;
    times[1] = buckPerProc;
    time_i = 2;

    omp_set_num_threads(proc);

    double startTime = omp_get_wtime();
    float* data = generateData(n);
    measureTime("Data generation", startTime); // no 3
 
    startTime = omp_get_wtime();
    float* sorted = bucketSort(data, proc, nPerProc, buckPerProc);
    measureTime("Total sort time", startTime); // no 8

    bool properlySorted = checkIfSorted(sorted, n);
    if (properlySorted) {
        cout << "Sorting worked." << std::endl;
        for (int i=0; i < 8; i++) {
            cout << times[i] << ((i == 7) ? "\n" : ",");
        }
    }
    else {
        cout << "Sorting didn't work." << std::endl;
        for (int i=0; i < 8; i++) {
            cout << times[i] << ((i == 7) ? "\n" : ",");
        }
    }
 
    return 0;
}
/*
* CPU,Bucket_CPU,Data_Gen,Init,Split,Sort,Merge,Total
*/
