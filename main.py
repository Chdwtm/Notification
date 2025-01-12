from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from utils.db_manager import DatabaseManager

# Load the KV file
Builder.load_file('notification_screen.kv')

class NotificationButton(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        super(NotificationButton, self).__init__(**kwargs)
        self.orientation = 'vertical'

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.parent.parent.edit_notification(self.text)
        return super(NotificationButton, self).on_touch_down(touch)

class NotificationScreen(BoxLayout):
    notification_list = ObjectProperty(None)

    def load_notifications(self):
        self.notification_list.data = []
        db = DatabaseManager()
        notifications = db.get_all_notifications()
        for notification in notifications:
            self.notification_list.data.append({'text': f"{notification['app_name']} - {notification['message']}"})

    def delete_notification(self, notification_text):
        db = DatabaseManager()
        notification_id = db.get_notification_id_by_message(notification_text)
        if notification_id:
            db.delete_notification(notification_id)
            self.load_notifications()

    def edit_notification(self, notification_text):
        content = EditNotificationPopup(notification_text=notification_text, save_callback=self.save_notification)
        self._popup = Popup(title="Edit Notification", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save_notification(self, old_text, new_text):
        db = DatabaseManager()
        notification_id = db.get_notification_id_by_message(old_text)
        if notification_id:
            db.update_notification(notification_id, new_text)
            self.load_notifications()
        self._popup.dismiss()

class EditNotificationPopup(BoxLayout):
    notification_text = StringProperty()
    save_callback = ObjectProperty()

    def __init__(self, notification_text, save_callback, **kwargs):
        super(EditNotificationPopup, self).__init__(**kwargs)
        self.notification_text = notification_text
        self.save_callback = save_callback

    def save(self):
        self.save_callback(self.notification_text, self.ids.edit_text.text)

class NotificationApp(App):
    def build(self):
        return NotificationScreen()

if __name__ == '__main__':
    NotificationApp().run()