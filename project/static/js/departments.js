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

function DisplayList(items, wrapper, rows_per_page, page) {
	wrapper.innerHTML = "";
	page--;

	let start = rows_per_page * page;
	let end = start + rows_per_page;
	let paginatedItems = items.slice(start, end);
	for (let i = 0; i < paginatedItems.length; i++) {
		let item = paginatedItems[i];

		const template = document.getElementById("department_template");
		const item_element = template.content.cloneNode(true);
		item_element.querySelector(".col").id = "dept_" + item.name;
		item_element.querySelector(".card-title").innerText = item.name;
		item_element.querySelector(".department-num-employees").innerText = item.num_employees + " Employees"
		item_element.querySelector(".department-avg-salary").innerText = "Average Salary: " + item.avg_salary + "$";
		item_element.querySelector(".view-button").href = endpoints['department_view'] + item.name;
		item_element.querySelector(".edit-button").addEventListener("click", () => {

			const edit_modal = document.getElementById("editModal")
			let edit_modal_without_listeners = edit_modal.cloneNode(true)
			edit_modal.parentNode.replaceChild(edit_modal_without_listeners, edit_modal)


			const new_name_input = edit_modal.querySelector("#editName")
			new_name_input.value = item.name
			edit_modal.querySelector("#editConfirmButton").addEventListener("click", () => {
				sendRequest("PUT", endpoints['departments_api'] + item.name,
					{"name": new_name_input.value}).then(() => {
						item.name = new_name_input.value
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
				sendRequest("DELETE", endpoints['departments_api'] + item.name).then(data => {
					items.splice(start+i, 1)
					DisplayList(items, wrapper, rows_per_page, (paginatedItems.length !== 1) ? page+1 : page)
					SetupPagination(items, pagination_element, rows)
				})
			})
		})


		wrapper.appendChild(item_element)
	}
}

function SetupPagination(items, wrapper, rows_per_page) {
	wrapper.innerHTML = "";

	let page_count = Math.ceil(items.length / rows_per_page);
	for (let i = 1; i < page_count + 1; i++) {
		let btn = PaginationButton(i, items);
		wrapper.appendChild(btn);
	}
}

function PaginationButton(page, items) {
	const template = document.getElementById("pagination_item_template");
	let button_template = template.content.cloneNode(true);
	button_template.querySelector('.page-link').innerText = page;
	let button = button_template.querySelector('.page-item')

	if (current_page === page) {
		button.classList.add('active')
	}


	button.addEventListener('click', () => {
		current_page = page;
		DisplayList(items, list_element, rows, current_page)

		let current_btn = document.querySelector('#pagination_div .active');
		current_btn.classList.remove('active')

		button.classList.add('active')
	})

	return button;
}

function buildPage() {
	sendRequest('GET', endpoints['departments_api'])
	.then(list_items => {
        DisplayList(list_items['departments'], list_element, rows, current_page)
        SetupPagination(list_items['departments'], pagination_element, rows)
    })


	const new_modal = document.getElementById("newModal")

	new_modal.querySelector("#newConfirmButton").addEventListener("click", () => {
		let name = new_modal.querySelector("#newName").value
		sendRequest("POST", endpoints['departments_api'] + name).then(() => {
			current_page = 1
			buildPage()
		})
	})
}

const list_element = document.getElementById('departments_list');
const pagination_element = document.getElementById('pagination_div');
