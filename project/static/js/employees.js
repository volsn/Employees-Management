function selectedDepartment(selector, selected) {
	let wrapper = document.getElementById(selector)
	for (let option of wrapper.children) {
		if (option.value === selected) {
			wrapper.removeChild(option)
			option.selected = true
			wrapper.insertBefore(option, wrapper.firstChild)
		}
	}
}

function DisplayList(items, wrapper, rows_per_page, page) {
	wrapper.innerHTML = ""
	page--

	let start = rows_per_page * page
	let end = start + rows_per_page
	let paginatedItems = items.slice(start, end)

	for (let i = 0; i < paginatedItems.length; i++) {
		let item = paginatedItems[i]
		item.index = i

		const template = document.getElementById("employee_template")
		const item_element = template.content.cloneNode(true)

		item_element.querySelector(".card-title").innerText = item.name
		item_element.querySelector(".birthdate").innerText = item.birthdate
		item_element.querySelector(".employee-salary").innerText = item.salary + "$"
		item_element.querySelector(".employee-department").innerText = item.department + " Department"
		item_element.querySelector(".view-button").href = endpoints['employee_view'] + item.id
		item_element.querySelector(".edit-button").addEventListener("click", () => {

			selectedDepartment("editDepartment", item.department)

			$("#editModal").modal("show")

			const edit_modal = document.getElementById("editModal")
			let edit_modal_without_listeners = edit_modal.cloneNode(true)
			edit_modal.parentNode.replaceChild(edit_modal_without_listeners, edit_modal)

			edit_modal.querySelector("#editName").value = item.name
			edit_modal.querySelector("#editBirthdate").value = item.birthdate
			edit_modal.querySelector("#editSalary").value = item.salary

			edit_modal.querySelector("#editConfirmButton").addEventListener("click", () => {

				let body = {
					name: edit_modal.querySelector("#editName").value,
					birthdate: edit_modal.querySelector("#editBirthdate").value,
					department: edit_modal.querySelector("#editDepartment").value,
					salary: edit_modal.querySelector("#editSalary").value
				}

				sendRequest("PUT", endpoints['employee_api'] + item.id, body).then(data => {
					item.salary = data.salary
					item.department = data.department
					item.name = data.name
					item.birthdate = data.birthdate

					DisplayList(items, wrapper, rows_per_page, page+1)
					SetupPagination(items, pagination_element, rows)
				})
			})

		})
		item_element.querySelector(".delete-button").addEventListener("click", () => {

			const delete_modal = document.getElementById("deleteModal")
			let delete_modal_without_listeners = delete_modal.cloneNode(true)
			delete_modal.parentNode.replaceChild(delete_modal_without_listeners, delete_modal)


			delete_modal.querySelector("#deleteConfirmButton").addEventListener("click", () => {
				sendRequest("DELETE", endpoints['employee_api'] + item.id).then(data => {
					items.splice(start+item.index, 1)
					DisplayList(items, wrapper, rows_per_page, (paginatedItems.length !== 1) ? page+1 : page)
					SetupPagination(items, pagination_element, rows)
				})
			})
		})

		wrapper.appendChild(item_element)
	}
}

function parseDate(date) {
	let [mm, dd, yyyy] = date.split(".")
	return new Date(yyyy, parseInt(mm) - 1, dd)
}

function SetupFilter(items) {
	const filterButton = document.getElementById("filter-button")
	const clearButton = document.getElementById("clear-filters-button")

	filterButton.addEventListener("click", () => {
		const born_on = document.getElementById("filterBornOn").value
		if (born_on) {
			const filtered_items = items.filter(item => { if (item.birthdate === born_on) return item })
			DisplayList(filtered_items, list_element, rows, 1)
        	SetupPagination(filtered_items, pagination_element, rows)
		}
		else {
			let born_start = document.getElementById("filterBornBetweenStart").value
			let born_end = document.getElementById("filterBornBetweenEnd").value

			if (born_start && born_end) {
				born_start = parseDate(born_start)
				born_end = parseDate(born_end)

				const filtered_items = items.filter(item => {
					let date = parseDate(item.birthdate)
					if (date >= born_start && date <= born_end)
						return item
				})
				DisplayList(filtered_items, list_element, rows, 1)
        		SetupPagination(filtered_items, pagination_element, rows)
			}
		}
	})

	clearButton.addEventListener("click", () => {
		document.getElementById("filterBornOn").value = null
		document.getElementById("filterBornBetweenStart").value = null
		document.getElementById("filterBornBetweenEnd").value = null
		DisplayList(items, list_element, rows, 1)
		SetupPagination(items, pagination_element, rows)
	})

}

function buildPage() {
	sendRequest('GET', endpoints['all_employees_api'])
	.then(list_items => {
        DisplayList(list_items['employees'], list_element, rows, current_page)
        SetupPagination(list_items['employees'], pagination_element, rows)
		SetupFilter(list_items['employees'])
    })

	createDepartmentOptions("editDepartment")
	createDepartmentOptions("newDepartment")

	const new_modal_button = document.getElementById("newModalButton")
	new_modal_button.addEventListener("click", () => {
		const new_modal = document.getElementById("newModal")

		new_modal.querySelector("#newConfirmButton").addEventListener("click", () => {

			let body = {
				"name": new_modal.querySelector("#newName").value,
				"birthdate": new_modal.querySelector("#newBirthdate").value,
				"department": new_modal.querySelector("#newDepartment").value,
				"salary": new_modal.querySelector("#newSalary").value
			}

			sendRequest("POST", endpoints['employee_api'], body).then(() => {
				current_page = 1
				buildPage()
				new_modal.querySelector("#newName").value = null
				new_modal.querySelector("#newBirthdate").value = null
				new_modal.querySelector("#newDepartment").value = null
				new_modal.querySelector("#newSalary").value = null
			})
		})
	})
}

const list_element = document.getElementById('employees_list')
const pagination_element = document.getElementById('pagination_div')
