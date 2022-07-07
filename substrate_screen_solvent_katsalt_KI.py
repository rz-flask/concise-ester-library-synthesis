#!/home/qcr/anaconda3/envs/rdk-env/bin/python
# coding: utf-8

from opentrons import protocol_api
metadata = {'apiLevel': '2.0'}

def run(protocol: protocol_api.ProtocolContext):
	# pipettes and tipracks
	tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul',4)

	p300_s = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack_1])

	# motor stirrer that holds kat salt
	stirred_plate = protocol.load_labware('custom_6x4_with_small_stirrer', 7)

	# 96 acids
	acid_plate = protocol.load_labware('custom_12x8_plastic_holder', 6)

	# trough holding KI
	trough = protocol.load_labware('custom_1x2_trough', 2)

	# reaction setup plate
	dest = protocol.load_labware('custom_12x8_reaction_plate',3)

	p300_s.well_bottom_clearance.dispense = 20
	# lowered aspirate height since we're using the trough
	p300_s.well_bottom_clearance.aspirate = 3
	p300_s.flow_rate.aspirate = 75
	p300_s.flow_rate.dispense = 200

	KI_vol = 33
	kat_vol = 33
	solvent_vol = 100

	# if False, return tip to tiprack
	trash = True

	wells_order = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
	 			   'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
	 			   'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',
	 			   'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',
	 			   'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
	 			   'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
	 			   'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',
	 			   'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12']

	vols_order = [400,359,383,392,318,365,273,329,304,359,336,362,
				  388,297,307,279,416,413,642,444,305,403,310,362,
				  435,531,366,429,368,286,429,294,336,264,311,280,
				  408,277,293,387,333,473,244,358,304,549,527,340,
				  322,340,325,307,284,264,304,356,498,420,463,273,
				  264,539,193,306,367,640,120,272,244,359,227,252,
				  255,314,290,349,269,280,332,289,477,254,382,264,
				  352,266,225,283,232,274,365,317,355,434,433,287]


	print("adding solvent from trough to acid plate")
	p300_s.transfer(
		vols_order,
        trough['A1'],
        [acid_plate.wells_by_name()[well_name] for well_name in wells_order],
	    new_tip='once', air_gap=10,blow_out_location="source well",trash=trash)

	protocol.pause("solvent transfer done")

	print("transferring kat salt from stirrer to reactor")
	p300_s.distribute(kat_vol,
        stirred_plate['A2'],
        dest.wells(),
	    new_tip='once', air_gap=10,trash=trash)

	protocol.pause("kat salt transfer done")

	print("transferring KI")
	p300_s.transfer(KI_vol,
	stirred_plate['A1'],
	dest.wells(),
	new_tip='once', air_gap=10,trash=trash)
