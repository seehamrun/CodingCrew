var allDays = document.querySelectorAll('.date');

for (var i = 0; i < allDays.length; i++) {
    allDays[i].addEventListener('click', () => {
      console.log('click');
  });
}
