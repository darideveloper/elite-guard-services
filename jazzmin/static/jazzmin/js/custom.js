// Global styles
const menuItems = document.querySelectorAll('.d-sm-inline-block a.nav-link')
menuItems.forEach(item => {
  item.classList.add('btn')
  item.classList.add('btn-primary')
  item.classList.add('text-light')
})
