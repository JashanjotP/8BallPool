$(document).ready(function() {
    let cueBall, cue, table;
    let isDrawing = false;

    

    function bindEventHandlers() {
        cueBall = $('svg circle[fill="WHITE"]');
        cue = $('svg line');
        table = $('svg');

        

        cueBall.on('mousedown', function(e) {
            isDrawing = true;

            cue.attr('x1', cueBall.attr("cx"));
            cue.attr('y1', cueBall.attr("cy"));
            cue.attr('x2', cueBall.attr("cx"));
            cue.attr('y2', cueBall.attr("cy"));
            cue.show();
        });

        $(document).on('mousemove', function(e) {
            if (!isDrawing) return;

            const { clientX, clientY } = e;
            const { left, top } = table.offset();

            const svgWidth = table.width();
            const svgHeight = table.height();
            const viewBoxWidth = 1400;
            const viewBoxHeight = 2750;

            const scaledX = ((clientX - left) / svgWidth) * viewBoxWidth;
            const scaledY = ((clientY - top) / svgHeight) * viewBoxHeight;

            cue.attr('x2', scaledX);
            cue.attr('y2', scaledY);
        });

        $(document).on('mouseup', function(e) {
            if (isDrawing) {
                cue.hide();
                const { clientX, clientY } = e;
                const { left, top } = table.offset();

                const svgWidth = table.width();
                const svgHeight = table.height();
                const viewBoxWidth = 1400;
                const viewBoxHeight = 2750;

                const scaledX = ((clientX - left) / svgWidth) * viewBoxWidth;
                const scaledY = ((clientY - top) / svgHeight) * viewBoxHeight;

                const dx = (scaledX - cueBall.attr("cx")) * 3;
                const dy = (scaledY - cueBall.attr("cy")) * 3;


                $.post("data.html",
                    JSON.stringify({
                        velx: dx.toString(),
                        vely: dy.toString()
                    }),
                    function(res) {
                        let i = 0; // Initialize counter for array iteration

                        function processItem() {
                            if (i < res.length) {
                                let item = res[i];
                                
                                // Find the previous SVG element and replace its content
                                $("svg").replaceWith(item)

                                bindEventHandlers()

                                i++; // Increment counter

                                setTimeout(processItem, 10); // Wait 0.01 second before next iteration
                            }else{
                                $.get("info",
                                function(data){
                                    console.log(data)
                                    const currentPlayer = data[0]
                                    const player1assigned = data[1]
                                    const player2assigned = data[2]
                                    const winner = data[3]

                                    console.log("Player 1 Balls:" +data[4])
                                    console.log("Player 2 Balls:" +data[5])


                                    if(winner !== null){
                                        $(".win-name").html(winner)
                                        $(".win-con.passive").removeClass("passive");
                                        return
                                    }

                                    if (player1assigned !== null){
                                        $("#player-1-hORl").html(player1assigned)
                                        $("#player-2-hORl").html(player2assigned)
                                    }

                                    if (currentPlayer == 0){

                                        const name = $("#player1-name-select")
                                        const image = $("#player1-image")
                                        const name2 = $("#player2-name-select")
                                        const image2 = $("#player2-image")


                                        if (name.hasClass("uncurrent-1")) {
                                            name.removeClass("uncurrent-1").addClass("current-1");
                                            image.removeClass("passive")
                                            name2.removeClass("current-2").addClass("uncurrent-2");
                                            image2.addClass("passive")
                                        }
                                        
                                    }else{

                                        const name = $("#player1-name-select")
                                        const image = $("#player1-image")
                                        const name2 = $("#player2-name-select")
                                        const image2 = $("#player2-image")


                                        if (name2.hasClass("uncurrent-2")) {
                                            name2.removeClass("uncurrent-2").addClass("current-2");
                                            image2.removeClass("passive")
                                            name.removeClass("current-1").addClass("uncurrent-1");
                                            image.addClass("passive")
                                        }

                                    }
                                })
                            }
                        }

                        processItem(); // Start the iteration
                        
                    }
                );

                isDrawing = false;
            }
        });

        
    }

    bindEventHandlers()    

    

});
