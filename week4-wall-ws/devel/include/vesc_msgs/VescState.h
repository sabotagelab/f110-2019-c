// Generated by gencpp from file vesc_msgs/VescState.msg
// DO NOT EDIT!


#ifndef VESC_MSGS_MESSAGE_VESCSTATE_H
#define VESC_MSGS_MESSAGE_VESCSTATE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace vesc_msgs
{
template <class ContainerAllocator>
struct VescState_
{
  typedef VescState_<ContainerAllocator> Type;

  VescState_()
    : voltage_input(0.0)
    , temperature_pcb(0.0)
    , current_motor(0.0)
    , current_input(0.0)
    , speed(0.0)
    , duty_cycle(0.0)
    , charge_drawn(0.0)
    , charge_regen(0.0)
    , energy_drawn(0.0)
    , energy_regen(0.0)
    , displacement(0.0)
    , distance_traveled(0.0)
    , fault_code(0)  {
    }
  VescState_(const ContainerAllocator& _alloc)
    : voltage_input(0.0)
    , temperature_pcb(0.0)
    , current_motor(0.0)
    , current_input(0.0)
    , speed(0.0)
    , duty_cycle(0.0)
    , charge_drawn(0.0)
    , charge_regen(0.0)
    , energy_drawn(0.0)
    , energy_regen(0.0)
    , displacement(0.0)
    , distance_traveled(0.0)
    , fault_code(0)  {
  (void)_alloc;
    }



   typedef double _voltage_input_type;
  _voltage_input_type voltage_input;

   typedef double _temperature_pcb_type;
  _temperature_pcb_type temperature_pcb;

   typedef double _current_motor_type;
  _current_motor_type current_motor;

   typedef double _current_input_type;
  _current_input_type current_input;

   typedef double _speed_type;
  _speed_type speed;

   typedef double _duty_cycle_type;
  _duty_cycle_type duty_cycle;

   typedef double _charge_drawn_type;
  _charge_drawn_type charge_drawn;

   typedef double _charge_regen_type;
  _charge_regen_type charge_regen;

   typedef double _energy_drawn_type;
  _energy_drawn_type energy_drawn;

   typedef double _energy_regen_type;
  _energy_regen_type energy_regen;

   typedef double _displacement_type;
  _displacement_type displacement;

   typedef double _distance_traveled_type;
  _distance_traveled_type distance_traveled;

   typedef int32_t _fault_code_type;
  _fault_code_type fault_code;



  enum {
    FAULT_CODE_NONE = 0,
    FAULT_CODE_OVER_VOLTAGE = 1,
    FAULT_CODE_UNDER_VOLTAGE = 2,
    FAULT_CODE_DRV8302 = 3,
    FAULT_CODE_ABS_OVER_CURRENT = 4,
    FAULT_CODE_OVER_TEMP_FET = 5,
    FAULT_CODE_OVER_TEMP_MOTOR = 6,
  };


  typedef boost::shared_ptr< ::vesc_msgs::VescState_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::vesc_msgs::VescState_<ContainerAllocator> const> ConstPtr;

}; // struct VescState_

typedef ::vesc_msgs::VescState_<std::allocator<void> > VescState;

typedef boost::shared_ptr< ::vesc_msgs::VescState > VescStatePtr;
typedef boost::shared_ptr< ::vesc_msgs::VescState const> VescStateConstPtr;

// constants requiring out of line definition

   

   

   

   

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::vesc_msgs::VescState_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::vesc_msgs::VescState_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace vesc_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'vesc_msgs': ['/home/jesse/f110-2019-c/week4-wall-ws/src/f110-skeletons-spring2019/system/vesc/vesc_msgs/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::vesc_msgs::VescState_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::vesc_msgs::VescState_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::vesc_msgs::VescState_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::vesc_msgs::VescState_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::vesc_msgs::VescState_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::vesc_msgs::VescState_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::vesc_msgs::VescState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "81214bb4c1945e7c159bd76ec397ac04";
  }

  static const char* value(const ::vesc_msgs::VescState_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x81214bb4c1945e7cULL;
  static const uint64_t static_value2 = 0x159bd76ec397ac04ULL;
};

template<class ContainerAllocator>
struct DataType< ::vesc_msgs::VescState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "vesc_msgs/VescState";
  }

  static const char* value(const ::vesc_msgs::VescState_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::vesc_msgs::VescState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# Vedder VESC open source motor controller state (telemetry)\n\
\n\
# fault codes\n\
int32 FAULT_CODE_NONE=0\n\
int32 FAULT_CODE_OVER_VOLTAGE=1\n\
int32 FAULT_CODE_UNDER_VOLTAGE=2\n\
int32 FAULT_CODE_DRV8302=3\n\
int32 FAULT_CODE_ABS_OVER_CURRENT=4\n\
int32 FAULT_CODE_OVER_TEMP_FET=5\n\
int32 FAULT_CODE_OVER_TEMP_MOTOR=6\n\
\n\
float64 voltage_input        # input voltage (volt)\n\
float64 temperature_pcb      # temperature of printed circuit board (degrees Celsius)\n\
float64 current_motor        # motor current (ampere)\n\
float64 current_input        # input current (ampere)\n\
float64 speed                # motor electrical speed (revolutions per minute) \n\
float64 duty_cycle           # duty cycle (0 to 1)\n\
float64 charge_drawn         # electric charge drawn from input (ampere-hour)\n\
float64 charge_regen         # electric charge regenerated to input (ampere-hour)\n\
float64 energy_drawn         # energy drawn from input (watt-hour)\n\
float64 energy_regen         # energy regenerated to input (watt-hour)\n\
float64 displacement         # net tachometer (counts)\n\
float64 distance_traveled    # total tachnometer (counts)\n\
int32   fault_code\n\
";
  }

  static const char* value(const ::vesc_msgs::VescState_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::vesc_msgs::VescState_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.voltage_input);
      stream.next(m.temperature_pcb);
      stream.next(m.current_motor);
      stream.next(m.current_input);
      stream.next(m.speed);
      stream.next(m.duty_cycle);
      stream.next(m.charge_drawn);
      stream.next(m.charge_regen);
      stream.next(m.energy_drawn);
      stream.next(m.energy_regen);
      stream.next(m.displacement);
      stream.next(m.distance_traveled);
      stream.next(m.fault_code);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct VescState_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::vesc_msgs::VescState_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::vesc_msgs::VescState_<ContainerAllocator>& v)
  {
    s << indent << "voltage_input: ";
    Printer<double>::stream(s, indent + "  ", v.voltage_input);
    s << indent << "temperature_pcb: ";
    Printer<double>::stream(s, indent + "  ", v.temperature_pcb);
    s << indent << "current_motor: ";
    Printer<double>::stream(s, indent + "  ", v.current_motor);
    s << indent << "current_input: ";
    Printer<double>::stream(s, indent + "  ", v.current_input);
    s << indent << "speed: ";
    Printer<double>::stream(s, indent + "  ", v.speed);
    s << indent << "duty_cycle: ";
    Printer<double>::stream(s, indent + "  ", v.duty_cycle);
    s << indent << "charge_drawn: ";
    Printer<double>::stream(s, indent + "  ", v.charge_drawn);
    s << indent << "charge_regen: ";
    Printer<double>::stream(s, indent + "  ", v.charge_regen);
    s << indent << "energy_drawn: ";
    Printer<double>::stream(s, indent + "  ", v.energy_drawn);
    s << indent << "energy_regen: ";
    Printer<double>::stream(s, indent + "  ", v.energy_regen);
    s << indent << "displacement: ";
    Printer<double>::stream(s, indent + "  ", v.displacement);
    s << indent << "distance_traveled: ";
    Printer<double>::stream(s, indent + "  ", v.distance_traveled);
    s << indent << "fault_code: ";
    Printer<int32_t>::stream(s, indent + "  ", v.fault_code);
  }
};

} // namespace message_operations
} // namespace ros

#endif // VESC_MSGS_MESSAGE_VESCSTATE_H
