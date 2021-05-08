---
published: true
---
[![Benjamin Bannekat ](https://raw.githubusercontent.com/hamid-abbaszadeh/hamid-abbaszadeh.github.io/master/images/post7.jpg)](https://hamid-abbaszadeh.github.io/Trees-Algorithm/)

The usefulness of Dependency Injection is in that the implementation of a class is more flexible and independent by decreasing the amount of coupling between a client and another service. The exact decoupling is the removal of a client class’s dependency on the implementation of an interface, instead requiring the implementation to be passed in.

Let’s take a look at a class that requires a dependency and the class defining that dependency.

```cpp
#include <iostream>

class GasolineSource {
public:
    void FuelUp() = 0;
};

class GasStation : public GasolineSource {
public:
    void FuelUp(){
        std::cout << "Pumping gas at gas station" << std::endl;
    }
};

// Car is dependent on GasStation being defined in order to fuel up.
class Car {
    GasStation gasolineService;
public:
    Car(){ }
    void getGasoline() {
        std::cout << "Car needs more gasoline!" << std::endl;
        gasolineService.FuelUp();
    }
};
```

Here, the class Car is dependent on the definition for GasStation. Car cannot be defined without GasStation being defined and Car would need to be changed whenever the source of gasoline is changed, like to a can.

```cpp
#include <iostream>

class GasolineSource {
public:
    void FuelUp() = 0;
};

class FuelCan : public GasolineSource {
public:
    void FuelUp(){
        std::cout << "Pumping gas from fuel can" << std::endl;
    }
};

// Car is dependent on FuelCan being defined in order to fuel up.
class Car {
    FuelCan gasolineService;
public:
    Car(){ }
    void getGasoline() {
        std::cout << "Car needs more gasoline!" << std::endl;
        gasolineService.FuelUp();
    }
};
```
The solution for this issue is Dependency Injection. We can inject the implementation for GasolineSource at runtime and use runtime polymorphism to abstract away the explicit implementation of GasolineSource.

```cpp
#include <iostream>

class GasolineSource {
public:
    virtual void FuelUp() = 0;
    virtual ~GasolineSource() = default;
};

class GasStation : public GasolineSource {
public:
    virtual void FuelUp() {
        std::cout << "Pumping gas at gas station" << std::endl;
    }
};

class FuelCan : public GasolineSource {
public:
    virtual void FuelUp() {
        std::cout << "Pumping gas from fuel can" << std::endl;
    }
};

class Car {
    GasolineSource *gasolineService = nullptr;
public:
    // The dependency for a source of gasoline is passed in
    // through constructor injection
    // as opposed to hard-coded into the class definition.
    Car(GasolineSource *service)
    : gasolineService(service) {
        // If the dependency was not defined, throw an exception.
        if(gasolineService == nullptr){
            throw std::invalid_argument("service must not be null");
        }
    }
    void getGasoline() {
        std::cout << "Car needs more gasoline!" << std::endl;
        // Abstract away the dependency implementation with polymorphism.
        gasolineService->FuelUp();
    }
};
```

Here is some code in main showing how the dependencies were injected.

```cpp
int main() {
    GasolineSource *stationService = new GasStation();
    GasolineSource *canService = new FuelCan();

    // racecar is independent from the implementation of the fuel service.
    // a gas station service is injected.
    Car racecar(stationService);
    racecar.getGasoline();

    // dune buggy is independent from the implementation of the fuel service.
    // a fuel can service is injected.
    Car duneBuggy(canService);
    duneBuggy.getGasoline();

    delete stationService;
    delete canService;
    return 0;
}
```
Here is the output from running main, showing that the appropriate services were called based up the dependencies injected.

**Output**
```
$ ./main
Car needs more gasoline!
Pumping gas at gas station
Car needs more gasoline!
Pumping gas from fuel can
```
