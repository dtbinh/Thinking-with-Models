package py2NetLogo;

import py4j.GatewayServer;
import org.nlogo.headless.HeadlessWorkspace;

public class NetLogoBridge {
     
    HeadlessWorkspace ws;
     
    public NetLogoBridge() {
        ws = HeadlessWorkspace.newInstance();
    }
     
    /**
     * Load a NetLogo model file into the headless workspace.
     * @param path: Path to the .nlogo file to load.
     */
    public void openModel(String path) {
    	try {
    		ws.open(path);
    	} catch (Exception e) {
    		System.out.println(e);
    	}
    }
 
    /**
     * Send a command to the open NetLogo model.
     * @param command: NetLogo command syntax.
     */
    public void command(String command) {
    	try {
            ws.command(command);
    	} catch (Exception e) {
    		System.out.println(e);
    	}
    }
 
    /**
     * Get the value of a variable in the NetLogo model.
     * @param command: The value to report.
     * @return Floating point number
     */
    public Object report(String command, String type) {
    	try {
            return ws.report(command);
          //   if (type.equals("d")) {
    		    // return ws.report(command);
          //   } else if (type.equals("s")) {
          //       return (String)ws.report(command);
          //   } else if (type.equals("b")) {
          //       return (Boolean)ws.report(command);
          //   } else {
          //       System.out.println(type + " is not a valid type.");
          //       return 0.0;
          //   }
    	} catch (Exception e) {
    		System.out.println(e);
    		return 0.0;
    	}
    }

    /**
     * Dispose of the workspace, closing the thread.
      * @param 
      * @return Boolean value for success of disposal
      */
    public Boolean dispose() {
        try {
            ws.dispose();
            return true;
        } catch (Exception e) {
            System.out.println(e);
            return false;
        }
    }
     
    /**
     * Launch the Gateway Server.
     */
    public static void main(String[] args) {
        GatewayServer gs = new GatewayServer(new NetLogoBridge());
        gs.start();
        System.out.println("Server running");
    }
}