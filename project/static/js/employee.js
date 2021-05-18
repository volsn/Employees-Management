function sendRequest(method, url, body = null) {
    const request = {
        method: method,
        headers: {}
    }

    if (method === 'POST' || method === 'PUT') {
        request['body'] = JSON.stringify(body)
        request['headers']['Content-Type'] = 'application/json'
    }

    return fetch(url, request).then(response => {
        if (response.ok) {
            return response.json()
        }
        return response.json().then(err => {
			console.error(err)
		})
    })
}


function displayEmployeeInfo(employee) {
    /* Function that displays employee information on the webpage */

    document.getElementById("employee_name").innerText = employee.name
    document.getElementById("employee_birthdate").innerText = employee.birthdate
    document.getElementById("employee_department").innerText = employee.department + " Department"
    document.getElementById("employee_salary").innerText = "Salary " + employee.salary + " $"

    document.getElementById("editName").value = employee.name
    document.getElementById("editBirthdate").value = employee.birthdate
    document.getElementById("editDepartment").value = employee.department
    document.getElementById("editSalary").value = employee.salary
}


function createDepartmentOptions(select, current_dept) {
    /* Function that loads all existing departments from rest api
    *  and displays them in the drop down menu */
    sendRequest('GET', endpoints['departments_api']).then(data => {

        let wrapper = document.getElementById(select)
        wrapper.innerText = ""

        for (let dept of data['departments']) {

            const template = document.getElementById("option_select_tempate");
            let option = template.content.cloneNode(true);

            option.querySelector("option").value = dept.name
            option.querySelector("option").innerText = dept.name

            if (dept.name === current_dept) {
                console.log("inserted")
                wrapper.insertBefore(option, wrapper.firstChild)
            } else {
                wrapper.appendChild(option)
            }
        }
    })
}


function employeePageSetup() {
    /* Function that setups the page */

    sendRequest('GET', endpoints['employee_api'] + self_id).then(employee => {

        displayEmployeeInfo(employee)

        document.getElementById("deleteConfirmButton").addEventListener("click", () => {
            sendRequest("DELETE", endpoints['employee_api'] + self_id).then(() => {
                window.location.replace(endpoints['index']);
            })
        })

        document.querySelector(".edit-button").addEventListener("click", () => {

            const edit_modal = document.getElementById("editModal")

            createDepartmentOptions("editDepartment", employee.department)

            edit_modal.querySelector("#editConfirmButton").addEventListener("click", () => {
                let body = {
                    name: edit_modal.querySelector("#editName").value,
                    birthdate: edit_modal.querySelector("#editBirthdate").value,
                    department: edit_modal.querySelector("#editDepartment").value,
                    salary: edit_modal.querySelector("#editSalary").value
                }

                sendRequest("PUT", endpoints['employee_api'] + self_id, body)
                    .then(data => {
                        employee = data
                        displayEmployeeInfo(employee)
                    })
            })
        })
    })
}
