class AdminSetup {

  /**
   * Setup global data
   */
  constructor () {
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

        // Warning in the input field
        const curpField = document.querySelector(curpSelector)
        if (alertType === "danger") {
          curpField.classList.add('is-invalid')
        } else {
          curpField.classList.remove('is-invalid')
        }
      })
    }

  }

  /**
   * Run the functions for the current page
   */
  autorun () {
    const methods = {
      "asistencias semanales": this.setupWeeklyAssistance,
      "empleados": this.validateCurp
    }
    if (methods[this.currrentPage]) {
      methods[this.currrentPage].call(this)
    }   
  }
}

new AdminSetup()