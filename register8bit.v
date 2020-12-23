////////////////////////////////////////////////////////////////////////////////////////////////////
//
//    Filename: register8bit.v
// Description: Contains a basic 8-bit register with load control
//
//	***************************
//	* DO NOT MODIFY THIS FILE *
//	***************************
//
////////////////////////////////////////////////////////////////////////////////////////////////////

module register8bit(clock, load, ins, outs);
	input        clock;		// Register clock
	input        load;		// Synchronous active-high load control
	input  [7:0] ins;			// Parallel load inputs
	output [7:0] outs;		// Register state

// The reg declaration refers to a target of a procedural assignment.
// Don't worry about what that means.

	reg    [7:0] outs;

// On a positiVe edge on the clock, the register stores the ins value as its state IF THE LOAD SIGNAL IS HIGH.
// If the load signal is low on a positive clock edge, the state of the register remains unchanged.
	
	always@(posedge clock) begin
		if(load == 1'b1)
		   outs <= ins;
	end

endmodule
