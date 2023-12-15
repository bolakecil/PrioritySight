document.addEventListener('DOMContentLoaded', function() {
  // Sidebar toggle and close logic
  var sidebar = document.querySelector('.sidebar');
  var sideButton = document.querySelector('.sidebutton');

  sideButton.addEventListener('click', function() {
      sidebar.classList.toggle('open');
  });

  document.addEventListener('click', function(event) {
      var isClickInsideSidebar = sidebar.contains(event.target);
      var isClickInsideSideButton = sideButton.contains(event.target);

      if (!isClickInsideSidebar && !isClickInsideSideButton) {
          sidebar.classList.remove('open');
      }
  });

  // Form progression and validation logic
  const nextBtns = document.querySelectorAll(".next-button");
  const progress = document.getElementById("progress");
  const formSteps = document.querySelectorAll(".form-step");
  const progressSteps = document.querySelectorAll(".progress-step");
  const progressText = document.querySelector('.sidebar p:nth-of-type(2)'); // Selector for the Progress text element

  let formStepsNum = 0;

  nextBtns.forEach((btn, index) => {
      btn.addEventListener("click", (event) => {
          if(validateCurrentStep(formStepsNum)){
              formStepsNum++;
              updateFormSteps();
              updateProgressbar();
          } else {
              event.preventDefault(); // Prevent moving to the next step
              alert('Please fill in all the required fields.');
          }
      });
  });

  function validateCurrentStep(stepIndex) {
      const currentStep = formSteps[stepIndex];
      let allFilled = true;

      currentStep.querySelectorAll('input[required]').forEach(input => {
          if (!input.value) {
              allFilled = false;
          }
      });

      return allFilled;
  }

  function updateFormSteps() {
      formSteps.forEach((formStep) => {
          formStep.classList.contains("form-step-active") &&
          formStep.classList.remove("form-step-active");
      });

      if (formSteps[formStepsNum]) {
        formSteps[formStepsNum].classList.add("form-step-active");
      }
  }

  function updateProgressbar() {
    progressSteps.forEach((progressStep, idx) => {
        if (idx <= formStepsNum) {
            progressStep.classList.add("progress-step-active");
        } else {
            progressStep.classList.remove("progress-step-active");
        }
    });

    const progressActive = document.querySelectorAll(".progress-step-active");

    // Calculate progress percentage and ensure it does not exceed 100%
    let progressPercentage = ((progressActive.length - 1) / (progressSteps.length - 1)) * 100;
    progressPercentage = Math.min(progressPercentage, 100); // Ensures progress does not exceed 100%
    progress.style.width = progressPercentage + "%";

    // Update progress text
    progressText.textContent = `Progress: ${progressPercentage.toFixed(0)}%`;
}


  function getCurrentFormattedDate() {
      const today = new Date();
      const day = String(today.getDate()).padStart(2, '0');
      const month = String(today.getMonth() + 1).padStart(2, '0'); //January is 0
      const year = today.getFullYear().toString().substr(-2);
      
      return `${day}/${month}/${year}`;
  }

  function showResultSection() {
    const resultSection = document.querySelector('.queue-result');
    if (resultSection) {
        resultSection.style.display = 'flex'; // Show the result section
    }
}


function hideFormSection(){
    const formSection = document.querySelector('.form');
    if(formSection){
        formSection.style.display = 'none';
    }
}

const submitButton = document.querySelector('form button[type="submit"]');
if (submitButton) {
    submitButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent the default form submission
        submitForm();
    });
}

// Modify the existing submitForm function
function submitForm() {
    var formData = new FormData(document.querySelector('form'));

    fetch('/process', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(html => {
        // Update a specific part of the page with the response
        document.querySelector('.result').innerHTML = html; // Adjust this selector as needed
        hideFormSection();
        showResultSection();
        // Optionally, handle any additional logic after form submission
    })
    .catch(error => console.error('Error:', error));
}

const resetButton = document.querySelector('.reset-section');
    if (resetButton) {
        resetButton.addEventListener('click', (event) => {
            // Logic to reset the form or perform other actions
            event.preventDefault();
            console.log('Reset button clicked');
            // Reset form logic here
            resetForm();
        });
    }

    function resetForm() {
        // Your reset logic here
        document.querySelector('form').reset();
        console.log('Form reset');
    
        // Redirect to patient.html to restart the form
        window.location.href = '/patient'; // Adjust the URL as needed based on your folder structure
    }
    

  // Update the date element in the sidebar
  const dateElement = document.querySelector('.sidebar .current-date'); // Selector for the Date element
  dateElement.textContent = getCurrentFormattedDate();

    // Initialize progress on first load
    updateProgressbar();
  });
