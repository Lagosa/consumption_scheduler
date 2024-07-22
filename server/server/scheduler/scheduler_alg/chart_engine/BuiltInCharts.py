def draw_charts_from_model(model, folder):
    model.history.save_global_best_fitness_chart(filename="charts/" + folder + "/" + "gbfc", verbose=True)
    model.history.save_local_best_fitness_chart(filename="charts/" + folder + "/" + "lbfc", verbose=True)

    model.history.save_global_objectives_chart(filename="charts/" + folder + "/" + "goc", verbose=True)
    # model.history.save_local_objectives_chart(filename="charts/" + folder + "/" + "loc", verbose=True)

    model.history.save_runtime_chart(filename="charts/" + folder + "/" + "runtime", verbose=True)
    model.history.save_exploration_exploitation_chart(filename="charts/" + "/" + folder + "/" + "expl_expl", verbose=True)

    model.history.save_diversity_chart(filename="charts/" + folder + "/" + "diversity", verbose=True)
    # model.history.save_trajectory_chart(filename="charts/" + folder + "/" + "trajectory", verbose=True)