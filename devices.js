simcir.registerDevice('4BitRam',
    {
        "width": 600,
        "height": 400,
        "showToolbox": false,
        "devices": [
            {"id": "dev0", "label": "D-FF", "type": "D-FF", "x": 352, "y": 184},
            {"id": "dev1", "label": "D-FF", "type": "D-FF", "x": 352, "y": 72},
            {"id": "dev2", "label": "D-FF", "type": "D-FF", "x": 352, "y": 128},
            {"type": "Out", "id": "dev3", "x": 440, "y": 24, "label": "Out1"},
            {"type": "Out", "id": "dev4", "x": 440, "y": 72, "label": "Out2"},
            {"type": "Out", "id": "dev5", "x": 440, "y": 120, "label": "Out3"},
            {"type": "Out", "id": "dev6", "x": 440, "y": 168, "label": "Out4"},
            {"id": "dev7", "label": "Toggle", "state": {"on": false}, "type": "Toggle", "x": 152, "y": 24},
            {"id": "dev8", "label": "Toggle", "state": {"on": true}, "type": "Toggle", "x": 152, "y": 80},
            {"id": "dev9", "label": "Toggle", "state": {"on": false}, "type": "Toggle", "x": 152, "y": 128},
            {"type": "Toggle", "id": "dev10", "x": 152, "y": 184, "label": "Toggle", "state": {"on": false}},
            {"type": "PushOn", "id": "dev11", "x": 88, "y": 112, "label": "PushOn"},
            {"type": "In", "id": "dev12", "x": 224, "y": 24, "label": "1"},
            {"type": "In", "id": "dev13", "x": 224, "y": 72, "label": "2"},
            {"type": "In", "id": "dev14", "x": 224, "y": 128, "label": "3"},
            {"type": "In", "id": "dev15", "x": 224, "y": 184, "label": "4"},
            {"type": "In", "id": "dev16", "x": 224, "y": 232, "label": "On"},
            {"id": "dev17", "label": "DC", "type": "DC", "x": 24, "y": 112},
            {"type": "NOT", "id": "dev18", "x": 288, "y": 24, "label": "NOT"},
            {"type": "NOT", "id": "dev19", "x": 288, "y": 72, "label": "NOT"},
            {"id": "dev20", "label": "D-FF", "type": "D-FF", "x": 352, "y": 24},
            {"type": "NOT", "id": "dev21", "x": 288, "y": 128, "label": "NOT"},
            {"type": "NOT", "id": "dev22", "x": 288, "y": 184, "label": "NOT"}
        ],
        "connectors": [
            {"from": "dev0.in0", "to": "dev22.out0"},
            {"from": "dev0.in1", "to": "dev16.out0"},
            {"from": "dev1.in0", "to": "dev19.out0"},
            {"from": "dev1.in1", "to": "dev16.out0"},
            {"from": "dev2.in0", "to": "dev21.out0"},
            {"from": "dev2.in1", "to": "dev16.out0"},
            {"from": "dev3.in0", "to": "dev20.out1"},
            {"from": "dev4.in0", "to": "dev1.out1"},
            {"from": "dev5.in0", "to": "dev2.out1"},
            {"from": "dev6.in0", "to": "dev0.out1"},
            {"from": "dev7.in0", "to": "dev11.out0"},
            {"from": "dev8.in0", "to": "dev11.out0"},
            {"from": "dev9.in0", "to": "dev11.out0"},
            {"from": "dev10.in0", "to": "dev11.out0"},
            {"from": "dev11.in0", "to": "dev17.out0"},
            {"from": "dev12.in0", "to": "dev7.out0"},
            {"from": "dev13.in0", "to": "dev8.out0"},
            {"from": "dev14.in0", "to": "dev9.out0"},
            {"from": "dev15.in0", "to": "dev10.out0"},
            {"from": "dev16.in0", "to": "dev11.out0"},
            {"from": "dev18.in0", "to": "dev12.out0"},
            {"from": "dev19.in0", "to": "dev13.out0"},
            {"from": "dev20.in0", "to": "dev18.out0"},
            {"from": "dev20.in1", "to": "dev16.out0"},
            {"from": "dev21.in0", "to": "dev14.out0"},
            {"from": "dev22.in0", "to": "dev15.out0"}
        ]
    }
);