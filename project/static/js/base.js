String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

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
			let alert = $('.alert-danger')
			alert.text(err['message'].capitalize())
			alert.show()
			alert.fadeTo(2000, 500).slideUp(500, function(){
				alert.slideUp(500)
			});
		})
    })
}

function createDepartmentOptions(select, current_dept) {
    /* Function that loads all existing departments from rest api
    *  and displays them in the drop down menu */
    sendRequest('GET', endpoints['departments_api']).then(data => {

        let wrapper = document.getElementById(select)
        wrapper.innerText = ""

        for (let dept of data['departments']) {

            const template = document.getElementById("option_select_tempate")
            let option = template.content.cloneNode(true)

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

function SetupPagination(items, wrapper, rows_per_page) {
	wrapper.innerHTML = "";

	let page_count = Math.ceil(items.length / rows_per_page);
	for (let i = 1; i < page_count + 1; i++) {
		let btn = PaginationButton(i, items);
		wrapper.appendChild(btn);
	}
}

function PaginationButton(page, items) {
	const template = document.getElementById("pagination_item_template")
	let button_template = template.content.cloneNode(true)
	button_template.querySelector('.page-link').innerText = page
	let button = button_template.querySelector('.page-item')

	if (current_page === page) {
		button.classList.add('active')
	}


	button.addEventListener('click', () => {
		current_page = page
		DisplayList(items, list_element, rows, current_page)

		let current_btn = document.querySelector('#pagination_div .active')
		current_btn.classList.remove('active')

		button.classList.add('active')
	})

	return button
}
