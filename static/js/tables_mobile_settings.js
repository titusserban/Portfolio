// Get all the tables from the page
const tables = document.querySelectorAll("table");

// Check if there are any tables
if (tables) {
    tables.forEach((table) => {
        // Get all the table rows
        const bodyTrCollection = table.querySelectorAll('tbody tr');
        // Get all the table heads
        const th = table.querySelectorAll('th');
        // Create an array of the table heads
        const thCollection = Array.from(th);

        bodyTrCollection.forEach((tr) => {
            // Select each table data of each tbody tr
            let td = tr.querySelectorAll('td');
            // Create an array of all table data cells
            let tdCollection = Array.from(td);
            for (let j = 0; j < tdCollection.length; j++) {
                // Check if the length of the table head items is equal to the length of the table data cell items
                if (j === thCollection.length) {
                    continue;
                }
                // Get the values of the table head
                let headerLabel = thCollection[j].innerHTML;
                // Assign the values of the table head to each table data cell as data-label
                tdCollection[j].setAttribute('data-label', headerLabel);
            }
        })
    })
}