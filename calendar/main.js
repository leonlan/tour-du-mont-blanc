Papa.parse("availability.csv", {
    download: true,
    header: true,
    dynamicTyping: true, // converts data to numbers
    complete: function(results) {
        var data = results.data;
        var calendarElement = document.getElementById('calendar');

        var headerRow = document.createElement('tr');
        var collapseHeader = document.createElement('th'); // header for collapse column
        headerRow.appendChild(collapseHeader);
        results.meta.fields.forEach((field,index) => {
            var fieldCell = document.createElement('th');
            fieldCell.textContent = field;

            fieldCell.setAttribute('data-col', index);
            fieldCell.onclick = function() {
                var columnCells = document.querySelectorAll(`td[data-col="${index}"]`);
                columnCells.forEach(el => el.classList.toggle('minimized'));
                fieldCell.classList.toggle('minimized');
            };

            headerRow.appendChild(fieldCell);
        });
        document.querySelector('#calendar thead').appendChild(headerRow);

        for (let i = 0; i < data.length; i++) {
            var hotelRow = document.createElement('tr');

            var collapseCell = document.createElement('td'); // cell for collapse button
            var collapseButton = document.createElement('button');
            collapseButton.textContent = 'collapse'; 
            collapseButton.onclick = function(e) {
                hotelRow.classList.toggle('minimized');
                this.textContent = hotelRow.classList.contains('minimized') ? 'expand' : 'collapse';

                // Stop propagating the click to parent elements
                e.stopPropagation();
            };
            collapseCell.appendChild(collapseButton);
            hotelRow.appendChild(collapseCell);

            results.meta.fields.forEach((field, index) => {
                var bedCell = document.createElement('td');
                bedCell.textContent = data[i][field];
                bedCell.setAttribute('data-col', index);

                if (index > 0) {
                    if (data[i][field] > 0) {
                        bedCell.className = 'available';
                    } else {
                        bedCell.className = 'notavailable';
                    }
                }
                hotelRow.appendChild(bedCell);
            });

            document.querySelector('#calendar tbody').appendChild(hotelRow);
        }
        
        // Making the rows sortable
        $("#calendar tbody").sortable();
    }
});

