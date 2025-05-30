'use client'

import { useEffect, useState } from 'react';

export default function Home() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/data')
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  return (
    <main>
      <h1>Microservice data</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </main>
  );
}
