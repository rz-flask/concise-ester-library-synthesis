#!/home/qcr/anaconda3/envs/rdk-env/bin/python
# coding: utf-8

from opentrons import protocol_api
metadata = {'apiLevel': '2.0'}

def run(protocol: protocol_api.ProtocolContext):
	# pipettes and tipracks

	tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul',5)

	p300_m = protocol.load_instrument('p300_multi', 'right', tip_racks=[tiprack_2])

	# 96 acids
	acid_plate = protocol.load_labware('custom_12x8_plastic_holder', 6)

	# reaction setup plate
	dest = protocol.load_labware('custom_12x8_reaction_plate',3)

	p300_m.well_bottom_clearance.dispense = 20
	p300_m.well_bottom_clearance.aspirate = 3
	p300_m.flow_rate.aspirate = 75
	p300_m.flow_rate.dispense = 200


	trash = True

	p300_m.transfer(33,
	acid_plate.rows_by_name()['A'],
	dest.rows_by_name()['A'],
	# [dest.wells_by_name()[i] for i in ["A1","E1"]],
	new_tip="always",blow_out_location="source well",mix_before = (3,100),trash=trash)
