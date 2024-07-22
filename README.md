# Consumption scheduler


## Purpose of the project

With the increasing number of electricity-consuming devices, there is a **huge stress placed on the electrical grid** during peak hours. This project aims to **shift the consumption** of a residential building **from peak to off-peak hours** by making a **schedule for appliances**. The schedule is made trying to **approximate a target consumption curve** for a day, while **minimizing tenant discomfort**. In an enhanced version of the algorithm, it is able to **identify a minimum subset of apartments** that have to modify their consumption patterns, thus not affecting the whole building, so significantly improving comfort.

The scheduling algorithm is integrated into an application that is deployed at the electricity distributor company. It is used by an operator to upload the dataset corresponding to each building involved, start a scheduling process, evaluate the results, and download the schedule.


 ## Deployment information 
 
 The application can be deployed using Docker. The *docker-compose.yml* file provides the necessary configuration to create and connect the containers. 
 First, create a network over which the containers will communicate. You can use the provided scripts or the following command:

  ```
    docker network create --gateway 172.19.0.1 --subnet 172.19.0.0/24 licenta-network
  ```

  Remember to update the configuration file if you decide to rename the network or change its subnet.
  After the network is created restart the machine, and run the build the containers by running *docker-compose* from the folder containing the configuration file.
  


## Technical details

In addressing the objectives, I utilized the strengths of meta-heuristic algorithms for solving multi-objective problems. For the first objective, I used the Harris Hawks Optimization (HHO) algorithm (inspired by the haunting behavior of hawks) to schedule the use of appliances in each apartment. The aim here is to create a schedule that closely matches a given target consumption curve while accommodating tenants' preferred usage times. To evaluate how well the schedule approximates the target curve, I employed a weighted average based on the Euclidean distance evaluation function and the Pearson correlation coefficient. For assessing tenant comfort, I developed an evaluation function similar to the Predicted Mean Vote (PMV), commonly used for evaluating thermal sensation.
For the second objective, I designed a bi-level optimization method. After preprocessing, the dataset is passed to the upper level using a Genetic Algorithm (GA) (inspired by the process of natural evolution and selection), which selects a subset of apartments that need to adjust their consumption patterns. These selected apartments are then handled in the lower level using the previously mentioned HHO algorithm, see [optimization_process]

![alt text][optimization_process]

[optimization_process]: https://github.com/Lagosa/consumption_scheduler_server/blob/main/images/algorithm%20steps.png "Optimization process"

The optimization module was developed using the meta-heuristic algorithm implementation from the [mealpy library](https://github.com/thieu1995/mealpy). The front-end application was developed using Vue-js, while the back-end application uses the Django framework in Python. The architecture of the whole application can be seen in [system_architecture]


![alt text][system_architecture]

[system_architecture]: https://github.com/Lagosa/consumption_scheduler_server/blob/main/images/system%20architecture.png "System architecture"



