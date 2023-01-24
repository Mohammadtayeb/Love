// When the the page is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Look for the page that has element with q_submit
    if (document.getElementById('q_submit')){
        // Make it disaled first
        document.getElementById('q_submit').disabled = true;
        
        // For all of those elements assign event handler
        document.querySelectorAll('.q_class').forEach(item => {
            
            // When clicked make it abled
            item.addEventListener('change', event => {
              // handle click
              document.getElementById('q_submit').disabled = false;
            })
          })
    }
})
