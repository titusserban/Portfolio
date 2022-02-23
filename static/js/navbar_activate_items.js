const activePage = window.location.pathname;
const navLinks = document.querySelectorAll('nav ul li a').forEach(link => {
  if (link.href.includes(`${activePage}`) && (`${activePage}`).length > 3){
    link.classList.add('active-nav-item');
  } 
})


const dashLinks = document.querySelectorAll('.dashboard-container aside .sidebar a');
if (dashLinks) {
  dashLinks.forEach(link => {
    if(link.href.includes(`${activePage}`)){
      link.classList.add('active');
    }
  })
}



