/*
 * http://stackoverflow.com/questions/17568470/holding-android-bluetooth-connection-through-multiple-activities
 * Thank you Martin Belcher - Eigo.
*/

package matthewkleinsmith.jetsonremotecontrol;

import android.app.Application;
import android.content.Context;

public class cBaseApplication extends Application {

    private static cBaseApplication instance = null;

    public cBaseApplication() {instance = this;}

    public BluetoothServer theBluetoothServer;

    @Override
    public void onCreate()
    {
        super.onCreate();
        instance = this;
        theBluetoothServer = new BluetoothServer();
    }

    public static Context getInstance() {
        if (instance == null) instance = new cBaseApplication();
        return instance;
    }
}
