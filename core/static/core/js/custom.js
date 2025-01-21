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
   * Run the functions for the current page
   */
  autorun () {
    const methods = {
      "asistencias semanales": this.setupWeeklyAssistance
    }
    if (methods[this.currrentPage]) {
      methods[this.currrentPage].call(this)
    }   
  }
}

new AdminSetup()