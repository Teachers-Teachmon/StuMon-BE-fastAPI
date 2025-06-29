from data import alert as data

def get_alert(user_id: int) :
    return data.get_alert(user_id)

def update_alert(alert_id) :
    return data.update_alert(alert_id)


def delete_alert(user_id):
    return data.delete_alert(user_id)