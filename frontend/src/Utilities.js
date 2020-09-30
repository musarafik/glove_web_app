// var ec2Url = 'http://ec2-18-217-92-92.us-east-2.compute.amazonaws.com/';
const ec2Url = process.env.NODE_ENV === 'production' ? ec2Url : 'http://localhost:5000/'; 
export default ec2Url;