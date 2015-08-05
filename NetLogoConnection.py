from py4j.java_gateway import JavaGateway
import matplotlib.pyplot as plt

def run_model(bridge, density, steps):
    '''
    Run the forest fire model, and return the number of trees burned.
     
    Args:
        bridge: The NetLogoBridge Java object
        density: Integer density percent, from 0 to 100
        steps: How many steps to run 
     
    Returns:
        The number of trees burned, as a float.
    '''
    bridge.command("set density " + str(density))
    bridge.command("setup")
    bridge.command("repeat " + str(steps) + " [go]")
    return bridge.report("burned-trees")

def test_model(): 
    gw = JavaGateway() # New gateway connection
    bridge = gw.entry_point # The actual NetLogoBridge object 

    # Path to Forest Fire model:
    sample_models = "/opt/NetLogo/netlogo-5.0.5/models/Sample Models/"
    forest_fire = "Earth Science/Fire.nlogo"
    # Now, open the model file
    bridge.openModel(sample_models + forest_fire)

    burned_trees = [run_model(bridge, i, 100) for i in range(0,100)]
    fig, ax = plt.subplots(figsize=(8,6))
    ax.grid(True)
    ax.set_xlabel("% Density")
    ax.set_ylabel("# of Trees Burned")
    plt.plot(burned_trees, linewidth=2)
    plt.show()