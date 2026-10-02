# Supply Chain Optimization

A multi-period sustainable supply chain optimization project implemented in Python using the Gurobi Optimizer. The model considers economic, social, and environmental aspects of supply chain planning and was developed based on an academic study published in the *Journal of Cleaner Production*.

## Project Overview

This project implements a mathematical optimization model for sustainable supply chain planning. The model determines procurement, production, transportation, inventory, and distribution decisions while considering demand, capacity, social performance, and environmental constraints.

The model represents a supply chain consisting of suppliers, raw materials, production methods, products, a distribution center, and retailers across multiple planning periods.

## Supply Chain Structure

The implemented model includes:

- 2 suppliers
- 3 raw materials
- 3 products
- 2 production methods
- 1 distribution center
- 3 retailers
- 2 planning periods

## Objectives

The model focuses on three dimensions of sustainable supply chain management:

### Economic Objective

The main objective is to minimize total supply chain cost, including:

- Supplier-related costs
- Raw material procurement costs
- Production costs
- Transportation costs
- Inventory holding costs
- Shortage and surplus-related costs
- Production method change costs

### Social Performance

Social performance is incorporated into the model through a minimum successful delivery requirement.

An epsilon-constraint is used to define the minimum acceptable level of social performance.

### Environmental Impact

Environmental performance is considered through:

- Energy consumption
- Waste generation
- Environmental costs
- Production method selection

Environmental upper bounds are incorporated into the optimization model using epsilon-constraint parameters.

## Optimization Approach

The model is formulated as a Mixed-Integer Linear Programming (MILP) model and solved using the Gurobi Optimizer.

The model includes:

- Binary decision variables for supplier, delivery, and production method decisions
- Continuous variables for procurement, production, transportation, inventory, surplus, and shortage quantities
- Supplier capacity constraints
- Production capacity constraints
- Distribution center capacity constraints
- Retailer capacity constraints
- Raw material balance constraints
- Inventory balance constraints
- Demand constraints
- Shortage and surplus constraints
- Environmental constraints
- Production method selection constraints

The economic objective is optimized while social and environmental performance requirements are incorporated as constraints.

## Epsilon-Constraint Analysis

The project uses an epsilon-constraint approach to incorporate the social and environmental dimensions into the cost-minimization model.

Two main parameters are used:

- `epsilon2`: Minimum required social performance level
- `epsilon3`: Maximum allowable environmental impact and associated cost

Additional Python models are included to analyze the social and environmental objectives separately.

## Project Structure

```text
supply-chain-optimization/
│
main.supplychain.py
Main supply chain optimization model. The model minimizes total supply chain cost while satisfying social performance and environmental impact requirements.
supplychain.epsilon2.py
Model used to analyze the social performance objective and determine the achievable social performance level under the supply chain constraints.
supplychain.epsilon3.py
Model used to analyze the environmental objective and determine the environmental impact of the supply chain.
Technologies
- Python
- Gurobi Optimizer
- GurobiPy
- Mixed-Integer Linear Programming (MILP)
- Mathematical Optimization
- Epsilon-Constraint Method
- Sustainable Supply Chain Optimization
Academic Basis
This project is based on the mathematical modeling framework presented in:
Yaghoubi, M., & Dadmand, F. (2026).
"A multi-objective sustainable supply chain mathematical model considering environmental and social aspects: A case study of Taqdis Brand."
Journal of Cleaner Production, 545, 147717.
DOI: 10.1016/j.jclepro.2026.147717
The study develops a multi-objective mathematical model for sustainable supply chain planning by considering economic, environmental, and social aspects.
In this project, the academic supply chain problem was implemented and adapted as a computational optimization model using Python and Gurobi. The implementation represents multiple suppliers, raw materials, products, production methods, a distribution center, retailers, and multiple planning periods.
The implementation incorporates procurement, production, transportation, inventory, shortage, and surplus decisions while considering social performance and environmental impact constraints.
├── main.supplychain.py
├── supplychain.epsilon2.py
└── supplychain.epsilon3.py
