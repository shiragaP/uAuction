import QtQuick 2.0

ListView {
    anchors.fill: parent
    id: list
    spacing: -15
    model: pythonListModel
    orientation: Qt.Horizontal
    delegate:Rectangle {
        id: itemDelegate
        property int listX: x-list.contentX
        property real angleZ:-15+ (90 * listX)  / list.width       // 0 - 90 degrees
        transform: Rotation { origin.y: height / 2; origin.x: 150; axis { x: 0; y: 1; z: 0 } angle: angleZ}
        width: 300
        height: parent.height
        //border.color: "lightgray"
        //color: "#22000000"
        gradient: Gradient {
          GradientStop { position: 0.0
          color: "#F0F0F0"
          }
          GradientStop { position: 0.5
          color: "#000000"
          }
          GradientStop { position: 1.0
          color: "#FFFFFF"
          }
        }
        Image {
            id: imageItem
            height: parent.height; width: parent.width
            anchors.left: parent.left
            fillMode: Image.PreserveAspectFit
            smooth: true
            // deligate can directly ues ListElement role name
            source: modelData
        }

        Binding {
            target: itemDelegate
            property: "angleZ"
            value: 0
            when: !(list.moving || list.dragging)
        }

        Behavior on angleZ {
            NumberAnimation {duration: 200; to: 0}
            enabled: !(list.flicking || list.dragging)
        }

    }
}
