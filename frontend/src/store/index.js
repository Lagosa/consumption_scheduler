import {createStore} from "vuex";

const error_codes = {
    "OK": {type: "SUCCESS", text: "Dataset was saved!"},
    "OPERATION_PERFORMED": {type: "SUCCESS", text: "Operation performed!"},
    "TAKEN": {type: "ERROR", text: "Identifier taken!"},
    "INCOMPLETE": {type: "WARNING", text: "Fill all required fields!"},
    "WRONG_FORMAT": {type: "ERROR", text: "Invalid input received!"},
    "UNKNOWN_OPERATION": {type: "ERROR", text: "Invalid operation received!"},
    "UNKNOWN_DATASET": {type: "ERROR", text: "Invalid dataset selected!"},
}

export default createStore({
    state: {
        notifications: []
    },
    actions: {
        addNotification({commit}, notification) {
            commit("PUSH_NOTIFICATION", notification)
        },
        removeNotification({commit}, notificationId) {
            commit("REMOVE_NOTIFICATION", notificationId)
        },
        handleStatus({commit}, status) {
            let notification = error_codes[status]
            if (notification == null) {
                notification = {
                    type: "ERROR",
                    text: "Internal error (generic)!",
                }
            }

            commit("PUSH_NOTIFICATION", notification)
        },
        handleInternalError({commit}, error) {
            let text = "Internal error!"

            if (error.message === "Network Error") {
                text = "Server unavailable!"
            }

            commit("PUSH_NOTIFICATION", {
                type: "ERROR",
                text: text,
            })
        },
    },
    mutations: {
        PUSH_NOTIFICATION(state, notification) {
            const notificationWithId  = {
                ...notification,
                id: (Math.random().toString(36) + Date.now().toString(36)).substring(3, 5)
            }

            state.notifications.push(notificationWithId)
        },
        REMOVE_NOTIFICATION(state, toRemoveId) {
            state.notifications = state.notifications.filter(notification => {
                return notification.id !== toRemoveId
            })
        }
    }
})