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

function employeePageSetup() {
    /* Function that setups the page */

    sendRequest('GET', endpoints['employee_api'] + self_id).then(employee => {

        displayEmployeeInfo(employee)

        document.getElementById("deleteConfirmButton").addEventListener("click", () => {
            sendRequest("DELETE", endpoints['employee_api'] + self_id).then(() => {
                window.location.replace(endpoints['index'])
                console.info('Employee removed')
                showInfoMessage('Employee removed')
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
                        console.info('Employee data updated')
						showInfoMessage('Employee data updated')
                    })
            })
        })
    })
}
