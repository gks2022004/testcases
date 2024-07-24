import { useState, useEffect } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:5000');

function App() {
  const [testcases, setTestcases] = useState([]);
  const [allTestcases, setAllTestcases] = useState([]);
  const [newTestcase, setNewTestcase] = useState({ name: '', description: '', status: false });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchTestcases();

    socket.on('update', (data) => {
      if (data.action === 'create') {
        setTestcases(prevTestcases => [...prevTestcases, data.testcase]);
        setAllTestcases(prevTestcases => [...prevTestcases, data.testcase]);
      } else if (data.action === 'update') {
        setTestcases(prevTestcases =>
          prevTestcases.map(tc => tc.id === data.testcase.id ? data.testcase : tc)
        );
        setAllTestcases(prevTestcases =>
          prevTestcases.map(tc => tc.id === data.testcase.id ? data.testcase : tc)
        );
      } else if (data.action === 'delete') {
        setTestcases(prevTestcases => prevTestcases.filter(tc => tc.id !== data.id));
        setAllTestcases(prevTestcases => prevTestcases.filter(tc => tc.id !== data.id));
      }
    });

    return () => {
      socket.off('update');
    };
  }, []);

  const fetchTestcases = async () => {
    try {
      const response = await axios.get('http://localhost:5000/testcases');
      setTestcases(response.data.testcases);
      setAllTestcases(response.data.testcases);
    } catch (error) {
      console.error('Error fetching testcases:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNewTestcase(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    if (e.target.value === '') {
      setTestcases(allTestcases);
    }
  };

  const handleSearch = () => {
    if (searchTerm.trim() === '') {
      setTestcases(allTestcases);
    } else {
      const filteredTestcases = allTestcases.filter(tc =>
        tc.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setTestcases(filteredTestcases);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/testcases', newTestcase);
      setNewTestcase({ name: '', description: '', status: false });
    } catch (error) {
      console.error('Error creating testcase:', error);
    }
  };

  const handleUpdate = async (id, updatedTestcase) => {
    try {
      await axios.put(`http://localhost:5000/testcases/${id}`, updatedTestcase);
    } catch (error) {
      console.error('Error updating testcase:', error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/testcases/${id}`);
    } catch (error) {
      console.error('Error deleting testcase:', error);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Test Cases</h1>
        <div style={{ marginBottom: '20px' }}>
          <input
            type="text"
            value={searchTerm}
            onChange={handleSearchChange}
            placeholder="Search test cases"
            style={{ marginRight: '10px', padding: '5px',height:'25px', width: '350px' }}
          />
          <button
            onClick={handleSearch}
            style={{ padding: '5px 10px' }}
          >
            Search
          </button>
        </div>
        <form onSubmit={handleSubmit} className="form">
          <input
            type="text"
            name="name"
            value={newTestcase.name}
            onChange={handleInputChange}
            placeholder="Test case name"
            required
          />
          <input
            type="text"
            name="description"
            value={newTestcase.description}
            onChange={handleInputChange}
            placeholder="Description"
            required
          />
          <label style={{ color: 'white' }}>
            Status:
            <input
              type="checkbox"
              name="status"
              checked={newTestcase.status}
              onChange={handleInputChange}
            />
          </label>
          <button type="submit">Add Test Case</button>
        </form>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {testcases.map(testcase => (
                <tr key={testcase.id}>
                  <td>{testcase.name}</td>
                  <td>{testcase.description}</td>
                  <td>
                    <input
                      type="checkbox"
                      checked={testcase.status}
                      onChange={(e) => handleUpdate(testcase.id, { ...testcase, status: e.target.checked })}
                    />
                  </td>
                  <td>
                    <button onClick={() => handleDelete(testcase.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;
