class AdminSetup {

  /**
   * Setup global data
   */
  constructor() {
    this.currrentPage = document.querySelector('h1').textContent.toLowerCase().trim()
    console.log(this.currrentPage)
    this.autorun()
  }

  /**
   * Set the value of a text input field
   * @param {string} inputName - The name of the input field (select)
   * @param {string} inputValue  - The value to set the input field to
   */
  #selectDropdownOption(selectName, optionValue) {
    const select = document.querySelector(`select[name="${selectName}"]`)
    if (select) {
      select.value = optionValue
    }
  }

  /**
   * Select all the registers in the current page
   */
  #selectAllRegisters() {
    document.querySelector('#action-toggle').click()
  }

  /**
   * Save a cookie
   * @param {string} name - The name of the cookie
   * @param {string} value - The value of the cookie
   */
  #saveCookie(name, value) {
    document.cookie = `${name}=${value}; path=/`
    console.log('save cookie')
  }

  /**
   * Delete a cookie
   * @param {string} name - The name of the cookie
   */
  #deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`
  }

  /**
   * Get cookie value
   * @param {string} name - The name of the cookie
   */
  #getCookie(name) {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.startsWith(name)) {
        return cookie.split('=')[1]
      }
    }
    return null
  }


  /**
   * Setup the weekly assistance page
   */
  setupWeeklyAssistance() {
    this.#selectDropdownOption('action', 'export_excel')
    setTimeout(() => {
      this.#selectAllRegisters()
    }, 200)
  }

  /**
   * Validate curp field with endpoint after update
   */
  validateCurp() {
    const curpSelector = "#id_curp"
    const curpInput = document.querySelector(curpSelector)
    if (curpInput) {
      curpInput.addEventListener('change', async () => {
        const curp = curpInput.value
        const response = await fetch(
          `/employees/api/validate-curp/`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ curp })
          },
        )
        const dataJson = await response.json()
        const message = dataJson.message
        let alertType = "success"
        if (!response.ok) {
          alertType = "danger"
        }

        // Get employee id if exists
        let employeeLink = ""
        if (dataJson.data && dataJson.data.employee_id) {
          const employeeId = dataJson.data.employee_id
          const employeeUrl = `/admin/employees/employee/${employeeId}/change/`
          employeeLink = `<a href="${employeeUrl}">Ver empleado</a>`
        }

        // Render message
        const alertHtml = `
          <div class="alert alert-${alertType} alert-dismissible">
            <button type="button" class="close" data-dismiss="alert" aria-hidden="true">x</button>
            <i class="icon fa fa-ban"></i>${message} ${employeeLink}
          </div>
        `
        const contentWrapper = document.querySelector('#content')
        const oldAlert = contentWrapper.querySelector('.alert')
        if (oldAlert) {
          oldAlert.remove()
        }
        contentWrapper.insertAdjacentHTML('afterbegin', alertHtml)

        // Warning in the input field and disable submit button
        const curpField = document.querySelector(curpSelector)
        const submitButton = document.querySelector('input[type="submit"]')
        console.log({ submitButton })
        if (alertType === "danger") {
          curpField.classList.add('is-invalid')
          submitButton.disabled = true
          submitButton.classList.add('disabled')
        } else {
          curpField.classList.remove('is-invalid')
          submitButton.disabled = false
          submitButton.classList.remove('disabled')
        }
      })
    }

  }

  /**
   * Create a new button to save and go back to assistance page
   */
  extrasGoBackButtonAssistance() {

    // Validate assistance queryparam
    const urlParams = new URLSearchParams(window.location.search)
    const fromAssistance = urlParams.get('assistance')
    console.log({ fromAssistance })

    // Render button
    if (fromAssistance) {
      console.log('Render button')
      const container = document.querySelector('#jazzy-actions')
      const saveButton = container.querySelector('.form-group:first-child')
      
      // Clone node as firts child
      const newButton = saveButton.cloneNode(true)
      newButton.querySelector('input').value = 'Guardar y regresar'
      container.insertAdjacentElement('afterbegin', newButton)

      // Save cookie when click the button
      newButton.addEventListener('click', () => {
        this.#saveCookie('back_to_assistance', 'true')
      })
    } else {
      // Go back to assistance page if cookie exists
      const backToAssistance = this.#getCookie('back_to_assistance')
      if (backToAssistance) {
        this.#deleteCookie('back_to_assistance')
        window.location.href = '/admin/assistance/assistance/'
      }
    }
  }


  /**
   * Run the functions for the current page
   */
  autorun() {
    const methods = {
      "asistencias semanales": this.setupWeeklyAssistance,
      "empleados": this.validateCurp,
      "extras": this.extrasGoBackButtonAssistance,
    }
    if (methods[this.currrentPage]) {
      methods[this.currrentPage].call(this)
    }
  }
}

new AdminSetup()