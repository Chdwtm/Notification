// NotificationListener.java
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;

public class NotificationListener extends NotificationListenerService {

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        String packageName = sbn.getPackageName();
        String notificationText = sbn.getNotification().tickerText != null ? sbn.getNotification().tickerText.toString() : "";
        String notificationTime = String.valueOf(sbn.getPostTime());

        // Send notification details to Python
        sendToPython(packageName, notificationText, notificationTime);
    }

    private void sendToPython(String app, String text, String time) {
        // JNI or other method to connect to Python component
    }
}