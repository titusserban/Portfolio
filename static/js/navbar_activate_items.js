// let primaryNavigation = document.getElementById("primary-navigation");
// let navItems = primaryNavigation.querySelectorAll('a');

// for (let navItemsIndex = 0; navItemsIndex < navItems.length; navItemsIndex++ ) {
//     navItems[navItemsIndex].addEventListener("click", function() {
//         let current = document.getElementsByClassName("active-nav-item");
//         current[0].className = current[0].className.replace(" active-nav-item");
//         this.className += " active-nav-item";
//     })
// }


// $(document).ready(function(){
//     $("#primary-navigation").on("click", "a", function(){
//         $("#primary-navigation a.active-nav-item").removeClass('active-nav-item');
//         $(this).addClass('active-nav-item');
//     })
// })


const activePage = window.location.pathname;
const navLinks = document.querySelectorAll('nav ul li a').forEach(link => {
  if (link.href.includes(`${activePage}`) && (`${activePage}`).length > 3){
    link.classList.add('active-nav-item');
  } 
  
})

