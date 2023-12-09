document.addEventListener('DOMContentLoaded', function() {
    var sidebar = document.querySelector('.sidebar');
    var sideButton = document.querySelector('.sidebutton');

    // Toggle sidebar on clicking the side button
    sideButton.addEventListener('click', function() {
        sidebar.classList.toggle('open');
    });

    // Close the sidebar when clicking outside of it
    document.addEventListener('click', function(event) {
        var isClickInsideSidebar = sidebar.contains(event.target);
        var isClickInsideSideButton = sideButton.contains(event.target);

        if (!isClickInsideSidebar && !isClickInsideSideButton) {
            sidebar.classList.remove('open');
        }
    });
});

const nextBtns = document.querySelectorAll(".next-button");
const progress = document.getElementById("progress");
const formSteps = document.querySelectorAll(".form-step");
const progressSteps = document.querySelectorAll(".progress-step");

let formStepsNum = 0;

nextBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    formStepsNum++;
    updateFormSteps();
    updateProgressbar();
  });
});

function updateFormSteps() {
  formSteps.forEach((formStep) => {
    formStep.classList.contains("form-step-active") &&
      formStep.classList.remove("form-step-active");
  });

  formSteps[formStepsNum].classList.add("form-step-active");
}

function updateProgressbar() {
  progressSteps.forEach((progressStep, idx) => {
    if (idx < formStepsNum + 1) {
      progressStep.classList.add("progress-step-active");
    } else {
      progressStep.classList.remove("progress-step-active");
    }
  });

  const progressActive = document.querySelectorAll(".progress-step-active");

  progress.style.width =
    ((progressActive.length - 1) / (progressSteps.length - 1)) * 98 + "%";
}