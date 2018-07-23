var allJanDays = document.querySelectorAll('.january');

for (var i = 0; i < allJanDays.length; i++) {
    allJanDays[i].addEventListener('click', () => {
      console.log('click');
  });
}
