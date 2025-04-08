#include <pybind11/pybind11.h>

namespace py = pybind11;
// using namespace std;
#include <iostream>
#include <vector>
#include <bitset>
#include <cmath>
#include <complex>
#include <unordered_map>
// #include <bits/stdc++.h>

typedef std::complex<double> Complex;
const int MAX_T = 64;  // Adjust to the maximum number of variables you will use

// Function to evaluate the polynomial equation
int eval_f(const std::vector<std::pair<int, std::vector<int>>>& terms, const bool* x, int t) {
    int val_out = 0;  // gets values between [0,7]
    
    for (const auto& term : terms) {
        int weight = term.first;
        const std::vector<int>& indices = term.second;
        
        bool v = true;  // Initialize to true (boolean "1")
        
        for (int j : indices) {
            v &= x[j];  // The variables are boolean, so this will remain boolean
        }
        
        val_out = (val_out + weight * static_cast<int>(v)) % 8;  // Ensure operations are modulo 8
    }
    
    return val_out;
}

// Function to get the truth table
void get_truthtable(const std::vector<std::pair<int, std::vector<int>>>& terms, int n, int t, const bool* initial_state, int* ttb) {
    if (n == t) {
        return;  // Base case (statevector handling)
    }

    int x_range = 1 << (t - n);  // 2^(t-n)
    bool x[MAX_T] = {false};     // Array to hold the values of x variables (initial state and other variables)
    
    // Fill the fixed values from the initial state
    for (int i = 0; i < n; ++i) {
        x[i] = initial_state[i];
    }
    
    // Loop through possible values for the remaining variables
    for (int i = 0; i < x_range; ++i) {
        // Fill the remaining variables (y variables)
        std::bitset<MAX_T> y_bin(i);
        for (int j = 0; j < (t - n); ++j) {
            x[n + j] = y_bin[j];
        }
        
        // Evaluate the function and store the result in the truth table
        ttb[i] = eval_f(terms, x, t);
    }
}

// Function to get the statevector from the truth table
void get_statevector(const int* ttb, int n, int t, const std::vector<int>& ovs, Complex* stvector) {
    int group_size = 1 << (t - n);  // Size of the truth table
    std::unordered_map<int, std::vector<int>> s_ldic;

    for (int k = 0; k < group_size; ++k) {
        int t_val = ttb[k];  // Truth table value for this combination of variables

        // Select the output variables corresponding to 'ovs'
        int chosen_int = 0;
        for (size_t i = 0; i < ovs.size(); ++i) {
            chosen_int |= ((k >> ovs[i]) & 1) << i;
        }

        if (s_ldic.find(chosen_int) == s_ldic.end()) {
            s_ldic[chosen_int] = std::vector<int>(8, 0);
        }

        s_ldic[chosen_int][t_val]++;
    }

    // Compute the statevector using FFT-like processing
    for (const auto& entry : s_ldic) {
        const std::vector<int>& counts = entry.second;
        Complex tmp0 = ((counts[1] - counts[5]) / std::sqrt(2), 0);
        Complex tmp1 = ((counts[3] - counts[7]) / std::sqrt(2), 0);
        Complex tmp2 = ( counts[0] - counts[4], 0 );
        Complex tmp3 = ( counts[2] - counts[6], 0 );
        Complex real_part = tmp2 + tmp0 - tmp1;
        Complex imag_part = tmp3 + tmp0 + tmp1;

        stvector[entry.first] = (real_part, imag_part) ;
    }

    // Normalize the statevector
    double normalization_factor = std::pow(2, 0.5 * (t - n));
    for (int i = 0; i < (1 << ovs.size()); ++i) {
        stvector[i] /= normalization_factor;
    }
}


PYBIND11_MODULE(example, m) {
    m.def("add", &get_truthtable, "A function that adds two numbers");
}



int main() {
    // Example usage
    std::vector<std::pair<int, std::vector<int>>> terms = {
        {1, {0, 2}},  // term with weight 1, indices [0, 2]
        {2, {1, 2}}   // term with weight 2, indices [1, 2]
    };

    bool initial_state[MAX_T] = {true, false, true};  // Example boolean vector

    int n = 2, t = 3;  // n = number of fixed variables, t = total number of variables
    int ttb[1 << (t - n)];  // Truth table

    // Generate truth table
    get_truthtable(terms, n, t, initial_state, ttb);

    // Output truth table for verification
    for (int i = 0; i < (1 << (t - n)); ++i) {
        std::cout << "ttb[" << i << "] = " << (int)ttb[i] << std::endl;
    }

    // Output the statevector
    std::vector<int> ovs = {0, 1};  // Output variable indices
    Complex stvector[1 << (t - n)];
    get_statevector(ttb, n, t, ovs, stvector);

    // Print statevector
    for (int i = 0; i < (1 << ovs.size()); ++i) {
        std::cout << "stvector[" << i << "] = " << stvector[i] << std::endl;
    }

    return 0;
}
