'use client'

import React, { useEffect, useState } from 'react'


const Landing = () => {
     const [data, setData] = useState<any>(null);
   
     useEffect(() => {
       fetch('http://localhost:5000/api/data')
         .then(res => res.json())
         .then(setData)
         .catch(console.error);
     }, []);
  return (
    <div>
      {data || "No data found"}
    </div>
  )
}

export default Landing
