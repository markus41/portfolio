export async function awaitHumanApproval(eventId: string): Promise<boolean> {
  console.log(`Awaiting human approval for ${eventId}`);
  return true; // stub
}
