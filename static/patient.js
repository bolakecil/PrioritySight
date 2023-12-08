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
