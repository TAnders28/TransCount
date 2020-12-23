////////////////////////////////////////////////////////////////////////////////////////////////////
//
//    Filename: buttonpress.v
// Description: This file creates an active-high signal that lasts for a single clock period after
//              an active-low button has been pressed then released.
//
// ***************************
// * DO NOT MODIFY THIS FILE *
// ***************************
//
////////////////////////////////////////////////////////////////////////////////////////////////////

module buttonpress(clock, in, out);
   input        clock;
	input        in;
	output       out;
	
	reg    [1:0] state;
	
	parameter KEY_UNPRESSED = 2'b00, KEY_PRESSED = 2'b01, KEY_RELEASED = 2'b10;

// This is the model for a Finite State Machine.
// - The DE-10 Lite pushbuttons are ACTIVE-LOW.
// - When the button is unpressed, the FSM is in the KEY_UNPRESSED state.
	
	always@(posedge clock) begin
		case(state)

// - In the KEY_UNPRESSED state, pressing the button causes a change to the KEY_PRSSED state on the next clock edge.

			KEY_UNPRESSED: begin
				if(in == 1'b0)
					state <= KEY_PRESSED;
			end

// - In the KEY_PRESSED state, releasing the button causes a change to the KEY_RELEASED state on the next clock edge.

			KEY_PRESSED: begin
				if(in == 1'b1)
					state <= KEY_RELEASED;
			end


// - In the KEY_RELEASED state, the next clock edge causes a change to the KEY_UNPRESSED state.

			KEY_RELEASED: begin
				state <= KEY_UNPRESSED;
			end
		endcase
	end
	
// Out is logic-1 during the single clock period when the FSM is in the KEY_RELEASED state.
// In all other instances, out is logic-0.

	assign out = (state == KEY_RELEASED);
	
endmodule
