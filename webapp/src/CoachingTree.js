import CoachingSearch from "./CoachingSearch";

function CoachingTree() {
  return (
    <>
      <h1>Coaching Tree</h1>
      <CoachingSearch onSelect={(coach) => console.log(`Selected ${coach}`)} />
    </>
  );
}

export default CoachingTree;
