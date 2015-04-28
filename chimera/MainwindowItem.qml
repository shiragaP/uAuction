import QtQuick 2.4
import QtQuick.Controls 1.2

Button {
    id: button1
    width: 160
    height: 240
    text: qsTr("Button")
    onClicked: link.debug("wasdsd")

    Image {
        id: image1
        x: 0
        y: 0
        width: 160
        height: 176
        fillMode: Image.PreserveAspectFit
        smooth: true
        source: "Image10_958642.jpg"

        Text {
            id: text1
            x: 0
            y: 177
            width: 160
            height: 26
            text: qsTr("Text")
            font.pixelSize: 12
        }
    }

    Button {
        id: button2
        x: 8
        y: 209
        width: 69
        height: 23
        text: qsTr("Button")
    }

    Button {
        id: button3
        x: 83
        y: 209
        width: 69
        height: 23
        text: qsTr("Button")
    }
}




