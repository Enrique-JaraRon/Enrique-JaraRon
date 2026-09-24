#include <cmath>
#include <iostream>
#include <stdexcept>
#include <string>

double normal_cdf(double x) {
    return 0.5 * std::erfc(-x / std::sqrt(2.0));
}

double black_scholes_price(
    double spot,
    double strike,
    double maturity,
    double rate,
    double volatility,
    const std::string& option_type
) {
    if (spot <= 0.0 || strike <= 0.0) {
        throw std::invalid_argument("spot and strike must be strictly positive");
    }
    if (maturity <= 0.0 || volatility <= 0.0) {
        throw std::invalid_argument("maturity and volatility must be strictly positive");
    }

    const double d1 =
        (std::log(spot / strike) +
         (rate + 0.5 * volatility * volatility) * maturity) /
        (volatility * std::sqrt(maturity));

    const double d2 = d1 - volatility * std::sqrt(maturity);

    if (option_type == "call") {
        return spot * normal_cdf(d1)
             - strike * std::exp(-rate * maturity) * normal_cdf(d2);
    }

    if (option_type == "put") {
        return strike * std::exp(-rate * maturity) * normal_cdf(-d2)
             - spot * normal_cdf(-d1);
    }

    throw std::invalid_argument("option_type must be call or put");
}

int main() {
    const double call = black_scholes_price(
        100.0, 100.0, 1.0, 0.03, 0.20, "call"
    );

    std::cout << "European call price: " << call << '\n';
    return 0;
}
