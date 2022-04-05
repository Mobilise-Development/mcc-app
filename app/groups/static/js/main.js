function setEventListeners() {
    let openForm = document.getElementsByClassName("open-form")
    let closeForm = document.getElementsByClassName("close-form")
    let groups = document.getElementsByClassName("group")

    Array.from(openForm).forEach(function (el) {
        el.addEventListener("click", function (el) {
            toggleForm(el.target.value)
        })
    })
    Array.from(closeForm).forEach(function (el) {
        el.addEventListener("click", function (el) {
            toggleForm(el.target.parentElement.id)
        })
    })
    Array.from(groups).forEach(function (el) {
        el.addEventListener("click", function (el) {
            selectGroup(el.target, groups)
        })
    })
}

function toggleForm(formElement) {
    let element = document.getElementById(formElement)
    element.classList.toggle("hidden")
}

function selectGroup(source, groups) {
    for (let i = 0; i < groups.length; i++) {
        groups[i].parentElement.classList.remove("selected")
    }
    source.parentElement.classList.add("selected")
    setSelectValue(source.id)
    showAttendees()
    showEvents();
}

function showAttendees() {
    let selected_group = document.getElementsByClassName("selected")[0]
    let attendees = document.getElementsByClassName("attendees")
    for (let i = 0; i < attendees.length; i++) {
        if (attendees[i].value !== +selected_group.dataset.attendee) {
            attendees[i].style.display = "none"
        } else {
            attendees[i].style.display = "flex"
        }
    }
}

function showEvents() {
    if (document.getElementsByClassName("selected")[0]) {
        let selectedGroup = document.getElementsByClassName("selected")[0]
        let eventsDataset = selectedGroup.dataset.events
        let events = document.getElementsByClassName("events")
        for (let i = 0; i < events.length; i++) {
            let event = events[i]
            let dataset = event.dataset.eventpk
            console.log(dataset, eventsDataset)
            if (eventsDataset.includes(dataset)) {
                event.classList.remove("hidden")
            } else {
                event.classList.add("hidden")
            }
        }
    }
}

function setSelectValue(valueToSelect) {
    let element = document.getElementById("id_term");
    element.style.display = "none"
    element.value = valueToSelect;
}

window.addEventListener('load', () => {
    showEvents();
    showAttendees();
    setEventListeners();
});