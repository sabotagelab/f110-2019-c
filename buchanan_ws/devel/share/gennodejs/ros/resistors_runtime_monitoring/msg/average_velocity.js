// Auto-generated. Do not edit!

// (in-package resistors_runtime_monitoring.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class average_velocity {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.average = null;
    }
    else {
      if (initObj.hasOwnProperty('average')) {
        this.average = initObj.average
      }
      else {
        this.average = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type average_velocity
    // Serialize message field [average]
    bufferOffset = _serializer.float64(obj.average, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type average_velocity
    let len;
    let data = new average_velocity(null);
    // Deserialize message field [average]
    data.average = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'resistors_runtime_monitoring/average_velocity';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '711be0a796b85a8a1e109ae6a26ad085';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 average
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new average_velocity(null);
    if (msg.average !== undefined) {
      resolved.average = msg.average;
    }
    else {
      resolved.average = 0.0
    }

    return resolved;
    }
};

module.exports = average_velocity;
