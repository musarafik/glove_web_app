const ec2Url = process.env.NODE_ENV === 'production' ? 'http://ec2-52-14-145-8.us-east-2.compute.amazonaws.com:5000/' : 'http://localhost:5000/'; 
export default ec2Url;