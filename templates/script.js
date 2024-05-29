document.addEventListener("DOMContentLoaded", function() {
    // Function to update the graph image based on selected pintu_air
    window.updatePintuAir = function() {
        const pintuAir = document.getElementById("pintu-air").value;
        const graphPath = `./graph/${pintuAir.replace(' ', '_')}.png`; // Construct the graph path based on selected option

        // Update the graph image
        document.getElementById('floodgate-graph').src = graphPath;
        document.getElementById('floodgate-graph').alt = `Graph for ${pintuAir}`;
    }

    // Attach event listener to the select element
    document.getElementById("pintu-air").addEventListener("change", updatePintuAir);
});