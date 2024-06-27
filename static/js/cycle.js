var phrases = [
    "Fun fact: Python is named after a TV sketch series",
    "Did you know? Python was a hobby project",
    "A ‘jiffy’ is an actual unit of time, referring to 1/100th of a second",
    'The first number to be spelled using the letter "a" is "one thousand"'
];

document.getElementById('cycle-text').textContent = phrases[Math.floor(Math.random() * phrases.length)];
console.log(document.getElementById('cycle-text').textContent)